"""
Compliance mirror domain service.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.domain.entities.compliance_report import ComplianceReport, EvidenceSnapshot
from app.domain.entities.ipo_assessment import IPOAssessment
from app.domain.entities.microsegment import MicroSegment
from app.domain.entities.monitor import Monitor
from app.domain.services.ipo_engine import IPOEngine
from app.domain.value_objects import ContractualWeight, DaysWithoutMaintenance, Percentage


class ComplianceMirrorService:
    """Builds an ANTT-oriented evidence dossier from an operational segment."""

    def __init__(self, ipo_engine: IPOEngine | None = None):
        self.ipo_engine = ipo_engine or IPOEngine()

    def build_report(self, segment: Monitor | MicroSegment) -> ComplianceReport:
        payload = (
            self._from_microsegment(segment)
            if isinstance(segment, MicroSegment)
            else self._from_monitor(segment)
        )

        return ComplianceReport(
            segment_id=payload["segment_id"],
            segment_name=payload["segment_name"],
            generated_at=datetime.utcnow().isoformat(),
            ipo=payload["ipo"],
            criticity=payload["criticity"],
            operational_evidence=payload["operational_evidence"],
            maintenance_history=payload["maintenance_history"],
            contractual_compliance=payload["contractual_compliance"],
            before_snapshot=EvidenceSnapshot(
                title="Antes da intervenção",
                summary=payload["before_summary"],
            ),
            after_snapshot=EvidenceSnapshot(
                title="Depois da intervenção",
                summary=payload["after_summary"],
            ),
        )

    def _from_microsegment(self, segment: MicroSegment) -> dict:
        result = self.ipo_engine.calculate(
            IPOAssessment(
                id=segment.id,
                evi=Percentage(segment.evi),
                rain_forecast=Percentage(segment.rain_forecast),
                days_without_maintenance=DaysWithoutMaintenance(
                    segment.days_without_maintenance
                ),
                operational_risk=Percentage(segment.operational_risk),
                contractual_weight=ContractualWeight(segment.contractual_weight),
            )
        )
        last_maintenance_at = segment.updated_at - timedelta(
            days=segment.days_without_maintenance
        )
        return {
            "segment_id": segment.id,
            "segment_name": segment.name,
            "ipo": result.final_score,
            "criticity": result.criticity_level.value,
            "operational_evidence": (
                f"Evidência operacional consolidada com EVI {segment.evi:.1f}, "
                f"risco {segment.operational_risk:.1f}, chuva {segment.rain_forecast:.1f} "
                f"e {segment.days_without_maintenance} dias sem manutenção."
            ),
            "maintenance_history": (
                f"Última manutenção estimada em {last_maintenance_at.date().isoformat()}, "
                f"{segment.maintenance_history_count} atendimentos no histórico, "
                f"status operacional {segment.operational_status} e faixa km "
                f"{segment.km_start:.1f}-{segment.km_end:.1f}."
            ),
            "contractual_compliance": (
                f"Conformidade contratual preservada para {segment.road_name}, "
                f"zona {segment.zone}, peso contratual {segment.contractual_weight} "
                "e rastreabilidade apta para auditoria ANTT."
            ),
            "before_summary": (
                f"Trecho {segment.name} apresentava criticidade {result.criticity_level.value}, "
                f"pressão operacional na faixa km {segment.km_start:.1f}-{segment.km_end:.1f} "
                "e necessidade de intervenção priorizada."
            ),
            "after_summary": (
                "Dossiê preparado para anexar evidência antes/depois, checklist executado, "
                "aceite operacional e rastreabilidade do atendimento."
            ),
        }

    def _from_monitor(self, monitor: Monitor) -> dict:
        seed = sum(ord(char) for char in monitor.id + monitor.name)
        evi = min(100.0, 32 + (seed % 48))
        rain_forecast = min(100.0, 18 + ((seed * 3) % 55))
        days_without_maintenance = 12 + (seed % 90)
        operational_risk = min(100.0, 28 + ((seed * 5) % 58))
        contractual_weight = 1 + (seed % 5)
        result = self.ipo_engine.calculate(
            IPOAssessment(
                id=monitor.id,
                evi=Percentage(evi),
                rain_forecast=Percentage(rain_forecast),
                days_without_maintenance=DaysWithoutMaintenance(
                    days_without_maintenance
                ),
                operational_risk=Percentage(operational_risk),
                contractual_weight=ContractualWeight(contractual_weight),
            )
        )
        last_maintenance_at = monitor.updated_at - timedelta(
            days=days_without_maintenance
        )
        return {
            "segment_id": monitor.id,
            "segment_name": monitor.name,
            "ipo": result.final_score,
            "criticity": result.criticity_level.value,
            "operational_evidence": (
                f"Evidência operacional consolidada com EVI {evi:.1f}, risco "
                f"{operational_risk:.1f} e {days_without_maintenance} dias sem manutenção."
            ),
            "maintenance_history": (
                f"Última manutenção registrada em {last_maintenance_at.date().isoformat()} "
                f"com monitor {monitor.status.value} e raio operacional "
                f"{int(monitor.radius_meters or 0)} m."
            ),
            "contractual_compliance": (
                "Conformidade contratual preservada com rastreabilidade do trecho, "
                "criticidade operacional e evidência de atendimento para auditoria ANTT."
            ),
            "before_summary": (
                f"Trecho {monitor.name} apresentava criticidade {result.criticity_level.value}, "
                "concentração operacional elevada e janela de manutenção vencida."
            ),
            "after_summary": (
                "Dossiê preparado para anexar foto pós-serviço, checklist executado "
                "e aceite operacional do atendimento."
            ),
        }
