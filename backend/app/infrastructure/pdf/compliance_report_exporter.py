"""
Compliance report PDF exporter
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.domain.entities.compliance_report import ComplianceReport


class ComplianceReportExporter:
    """Exports compliance dossier as PDF"""

    def export(self, report: ComplianceReport) -> bytes:
        buffer = BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ComplianceTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=10,
        )
        section_style = ParagraphStyle(
            "ComplianceSection",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=colors.HexColor("#1d4ed8"),
            spaceAfter=8,
            spaceBefore=10,
        )
        body_style = ParagraphStyle(
            "ComplianceBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#1f2937"),
        )

        elements = [
            Paragraph("Dossiê Digital de Evidência - Compliance Mirror", title_style),
            Paragraph(
                f"Trecho atendido: {report.segment_name} ({report.segment_id})",
                body_style,
            ),
            Paragraph(f"Data: {report.generated_at}", body_style),
            Spacer(1, 8),
        ]

        summary_table = Table(
            [
                ["IPO", f"{report.ipo:.2f}", "Criticidade", report.criticity],
                [
                    "Conformidade contratual",
                    report.contractual_compliance,
                    "Evidência operacional",
                    report.operational_evidence,
                ],
            ],
            colWidths=[34 * mm, 42 * mm, 42 * mm, 62 * mm],
        )
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                    ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#eff6ff")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#93c5fd")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.extend([summary_table, Spacer(1, 8)])

        elements.extend(
            [
                Paragraph("Antes / Depois", section_style),
                self._snapshot_table(report, body_style),
                Paragraph("Histórico de manutenção", section_style),
                Paragraph(report.maintenance_history, body_style),
                Paragraph("Conformidade contratual", section_style),
                Paragraph(report.contractual_compliance, body_style),
            ]
        )

        document.build(elements)
        return buffer.getvalue()

    def _snapshot_table(
        self,
        report: ComplianceReport,
        body_style: ParagraphStyle,
    ) -> Table:
        table = Table(
            [
                [
                    Paragraph(f"<b>{report.before_snapshot.title}</b><br/>{report.before_snapshot.summary}", body_style),
                    Paragraph(f"<b>{report.after_snapshot.title}</b><br/>{report.after_snapshot.summary}", body_style),
                ]
            ],
            colWidths=[85 * mm, 85 * mm],
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#fef2f2")),
                    ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#ecfdf5")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        return table
