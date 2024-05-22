from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.conf import settings
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from django.utils.timezone import now
from reportlab.platypus import Image
import io
from datetime import datetime


def generate_invoice_pdf(user, speciality, transaction_code, price, description, payment_status):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title', fontSize=18, textColor=colors.blue, alignment=TA_LEFT)
    normal_style = styles['Normal']
    header_style = ParagraphStyle(
        name='Header', fontSize=14, textColor=colors.darkgrey, alignment=TA_LEFT)

    # Company Logo
    logo_path = "http://securitiespesa.com/images/logo.png"
    company_logo = Image(logo_path, width=100, height=50)

    # Company Contact Information
    contact_info = Paragraph(
        "Phone: +254 724 855305<br/>Email: info@securitiespesa.com<br/>Website: www.securitiespesa.com<br/>Address: David Osieli Road , Westlands Nairobi , Kenya", normal_style)

    # Invoice Title and Current Date
    invoice_title = Paragraph("INVOICE", title_style)
    current_date = Paragraph(
        f"Date: {datetime.now().strftime('%Y-%m-%d')}", normal_style)

    # Header table to align invoice title and current date horizontally
    header_table = Table([
        [company_logo, '', '', invoice_title],
        ['', '', '', current_date]
    ], colWidths=[letter[0] * 0.8 * 0.25, letter[0] * 0.8 * 0.05, letter[0] * 0.8 * 0.35, letter[0] * 0.8 * 0.35], rowHeights=[50, 20])

    # Adjusting Table Styles
    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]

    # Invoice Details Table
    invoice_details = [
        ["Concern", "Payment Status", "Transaction Code", "Amount"],
        [speciality.name, payment_status, transaction_code, f"Ksh {price}"]
    ]

    # Applying cell styles
    for row in range(len(invoice_details)):
        for col in range(len(invoice_details[0])):
            cell_style = [
                ('TEXTCOLOR', (col, row), (col, row), colors.black),
                ('LEFTPADDING', (col, row), (col, row), 5),
                ('RIGHTPADDING', (col, row), (col, row), 5),
            ]
            table_style.extend(cell_style)

    # Creating Table for Invoice Details without background colors
    table_width = 0.8 * letter[0]  # 80% width of the PDF
    table = Table(invoice_details, colWidths=[
                  table_width * 0.3, table_width * 0.2, table_width * 0.2, table_width * 0.3])
    table.setStyle(TableStyle(table_style))

    # Allow description to wrap
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))

    # Problem Description
    problem_description = Paragraph(
        f"Concern Description: {description}", normal_style)

    # Adding Elements to Document
    elements.extend([header_table, Spacer(1, 20),
                     contact_info, Spacer(1, 20),
                     table, Spacer(1, 20),
                     problem_description])

    doc.build(elements)
    buffer.seek(0)
    return buffer


def send_invoice_email(user, speciality, transaction_code, price, description, payment_status):
    subject = 'Your Payment Invoice'
    message = 'Please find attached your payment invoice.'
    email = user.email

    pdf_buffer = generate_invoice_pdf(
        user, speciality, transaction_code, price, description, payment_status)

    email_message = EmailMessage(
        subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    email_message.attach(
        'invoice.pdf', pdf_buffer.getvalue(), 'application/pdf')
    email_message.send()
    return True
