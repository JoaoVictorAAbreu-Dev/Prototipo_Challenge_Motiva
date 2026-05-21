"""
Operational clustering domain service
"""

from math import atan2, cos, radians, sin, sqrt
from uuid import uuid4

import numpy as np
from sklearn.cluster import DBSCAN

from app.domain.entities.intervention_cluster import (
    InterventionCluster,
    MicroSegment,
)


class ClusterGenerationService:
    """Creates intervention clusters from nearby critical microsegments"""

    EARTH_RADIUS_KM = 6371.0088
    DEFAULT_EPSILON_KM = 8.0
    DEFAULT_MIN_SAMPLES = 2
    FUEL_EFFICIENCY_KM_PER_LITER = 3.4
    AVERAGE_OPERATIONAL_SPEED_KMH = 42.0

    def generate(
        self,
        microsegments: list[MicroSegment],
        epsilon_km: float = DEFAULT_EPSILON_KM,
        min_samples: int = DEFAULT_MIN_SAMPLES,
        minimum_priority_score: float = 75.0,
    ) -> list[InterventionCluster]:
        if epsilon_km <= 0:
            raise ValueError("epsilon_km must be greater than zero")
        if min_samples < 1:
            raise ValueError("min_samples must be at least 1")

        eligible_segments = [
            segment
            for segment in microsegments
            if segment.priority_score >= minimum_priority_score
        ]

        if len(eligible_segments) < min_samples:
            return []

        coordinates_radians = np.radians(
            [[segment.latitude, segment.longitude] for segment in eligible_segments]
        )

        dbscan = DBSCAN(
            eps=epsilon_km / self.EARTH_RADIUS_KM,
            min_samples=min_samples,
            metric="haversine",
            algorithm="ball_tree",
        )
        labels = dbscan.fit_predict(coordinates_radians)

        clusters: list[InterventionCluster] = []
        unique_labels = sorted(label for label in set(labels) if label != -1)

        for label in unique_labels:
            grouped = [
                eligible_segments[index]
                for index, current_label in enumerate(labels)
                if current_label == label
            ]
            centroid_latitude = sum(item.latitude for item in grouped) / len(grouped)
            centroid_longitude = sum(item.longitude for item in grouped) / len(grouped)
            average_priority = round(
                sum(item.priority_score for item in grouped) / len(grouped), 2
            )

            total_km = round(
                sum(
                    self._distance_km(
                        item.latitude,
                        item.longitude,
                        centroid_latitude,
                        centroid_longitude,
                    )
                    for item in grouped
                )
                * 2,
                2,
            )
            baseline_km = round(total_km * 1.35, 2)
            estimated_operational_savings = round(max(baseline_km - total_km, 0.0), 2)
            estimated_fuel_saved_liters = round(
                estimated_operational_savings / self.FUEL_EFFICIENCY_KM_PER_LITER, 2
            )
            optimized_time_minutes = round(
                (estimated_operational_savings / self.AVERAGE_OPERATIONAL_SPEED_KMH) * 60,
                2,
            )

            clusters.append(
                InterventionCluster(
                    id=str(uuid4()),
                    centroid_latitude=round(centroid_latitude, 6),
                    centroid_longitude=round(centroid_longitude, 6),
                    microsegments=grouped,
                    total_km=total_km,
                    average_priority=average_priority,
                    estimated_operational_savings=estimated_operational_savings,
                    estimated_fuel_saved_liters=estimated_fuel_saved_liters,
                    optimized_time_minutes=optimized_time_minutes,
                )
            )

        return clusters

    def _distance_km(
        self,
        start_latitude: float,
        start_longitude: float,
        end_latitude: float,
        end_longitude: float,
    ) -> float:
        start_latitude_rad = radians(start_latitude)
        start_longitude_rad = radians(start_longitude)
        end_latitude_rad = radians(end_latitude)
        end_longitude_rad = radians(end_longitude)

        delta_latitude = end_latitude_rad - start_latitude_rad
        delta_longitude = end_longitude_rad - start_longitude_rad

        haversine = (
            sin(delta_latitude / 2) ** 2
            + cos(start_latitude_rad)
            * cos(end_latitude_rad)
            * sin(delta_longitude / 2) ** 2
        )
        arc = 2 * atan2(sqrt(haversine), sqrt(1 - haversine))
        return self.EARTH_RADIUS_KM * arc
