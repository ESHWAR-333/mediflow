from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def generate_booking_pdf(data: dict) -> bytes:

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontSize=22,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        fontName="Helvetica",
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
        spaceAfter=4
    )

    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#333333"),
    )

    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#111111"),
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=9,
        fontName="Helvetica",
        textColor=colors.HexColor("#999999"),
        alignment=TA_CENTER,
    )

    urgency_map = {
        5: ("CRITICAL", colors.HexColor("#d32f2f")),
        4: ("HIGH", colors.HexColor("#e64a19")),
        3: ("MEDIUM", colors.HexColor("#f57c00")),
        2: ("LOW", colors.HexColor("#388e3c")),
        1: ("ROUTINE", colors.HexColor("#1976d2")),
    }

    urgency_score = int(data.get("urgency_score", 1))
    urgency_label, urgency_color = urgency_map.get(urgency_score, ("ROUTINE", colors.HexColor("#1976d2")))

    story = []

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("🏥 MediFlow", title_style))
    story.append(Paragraph("Booking Confirmation", subtitle_style))
    story.append(Paragraph(
        f"Generated: {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}",
        subtitle_style
    ))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e0e0e0")))
    story.append(Spacer(1, 0.5*cm))

    details = [
        ["Booking ID",     data.get("booking_id", "—")],
        ["Patient ID",     data.get("patient_id", "—")],
        ["Doctor ID",      data.get("doctor_id", "—")],
        ["Preferred Time", data.get("preferred_time", "—")],
        ["Symptoms",       data.get("symptoms", "—")],
    ]

    table_data = [
        [Paragraph(row[0], label_style), Paragraph(str(row[1]), value_style)]
        for row in details
    ]

    table = Table(table_data, colWidths=[5*cm, 12*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f5f5f5")),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [colors.white, colors.HexColor("#fafafa")]),
        ("BOX",        (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("INNERGRID",  (0, 0), (-1, -1), 0.5, colors.HexColor("#eeeeee")),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.6*cm))

    urgency_data = [[
        Paragraph("Urgency Score", label_style),
        Paragraph(
            f'<font color="{urgency_color.hexval()}" size="11"><b>{urgency_score} — {urgency_label}</b></font>',
            value_style
        )
    ]]

    urgency_table = Table(urgency_data, colWidths=[5*cm, 12*cm])
    urgency_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#fff8e1")),
        ("BOX",           (0, 0), (-1, -1), 1, urgency_color),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))

    story.append(urgency_table)
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e0e0e0")))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(
        "This is an automatically generated confirmation. Please retain for your records.",
        footer_style
    ))
    story.append(Paragraph("MediFlow Healthcare Platform · mediflow.health", footer_style))

    doc.build(story)
    return buffer.getvalue()