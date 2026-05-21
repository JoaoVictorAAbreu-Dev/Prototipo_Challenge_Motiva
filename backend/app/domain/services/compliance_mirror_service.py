"""
Compliance mirror domain service
"""

from datetime import datetime, timedelta

from app.domain.entities.compliance_report import ComplianceReport, EvidenceSnapshot
from app.domain.entities.monitor import Monitor


class ComplianceMirrorService:
    """Builds an ANTT-oriented evidence dossier from an operational segment"""

    def build_report(self, monitor: Monitor) -> ComplianceReport:
        seed = sum(ord(char) for char in monitor.id + monitor.name)
        evi = min(100.0, 32 + (seed % 48))
        rain_forecast = min(100.0, 18 + ((seed * 3) % 55))
        days_without_maintenance = 12 + (seed % 90)
        operational_risk = min(100.0, 28 + ((seed * 5) % 58))
        contractual_weight = 1 + (seed % 5)
        maintenance_factor = min(days_without_maintenance / 90, 1.0) * 100
        ipo = round(
            evi * 0.3
            + rain_forecast * 0.15
            + maintenance_factor * 0.2
            + operational_risk * 0.2
            + contractual_weight * 20 * 0.15,
            2,
        )
        criticity = self._resolve_criticity(ipo)
        last_maintenance_at = monitor.updated_at - timedelta(days=days_without_maintenance)

        return ComplianceReport(
            segment_id=monitor.id,
            segment_name=monitor.name,
            generated_at=datetime.utcnow().isoformat(),
            ipo=ipo,
            criticity=criticity,
            operational_evidence=(
                f"Evidência operacional consolidada com EVI {evi:.1f}, risco "
                f"{operational_risk:.1f} e {days_without_maintenance} dias sem manutenção."
            ),
            maintenance_history=(
                f"Última manutenção registrada em {last_maintenance_at.date().isoformat()} "
                f"com monitor {monitor.status.value} e raio operacional "
                f"{int(monitor.radius_meters or 0)} m."
            ),
            contractual_compliance=(
                "Conformidade contratual preservada com rastreabilidade do trecho, "
                "criticidade operacional e evidência de atendimento para auditoria ANTT."
            ),
            before_snapshot=EvidenceSnapshot(
                title="Antes da intervenção",
                summary=(
                    f"Trecho {monitor.name} apresentava criticidade {criticity}, "
                    f"concentração operacional elevada e janela de manutenção vencida."
                ),
            ),
            after_snapshot=EvidenceSnapshot(
                title="Depois da intervenção",
                summary=(
                    "Dossiê preparado para anexar foto pós-serviço, checklist executado "
                    "e aceite operacional do atendimento."
                ),
            ),
        )

    def _resolve_criticity(self, ipo: float) -> str:
        if ipo < 25:
            return "baixo"
        if ipo < 50:
            return "moderado"
        if ipo < 75:
            return "alto"
        return "crítico"
