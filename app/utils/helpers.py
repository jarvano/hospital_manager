from flask import current_app
from flask_mail import Message
from app import mail
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

def send_email(subject, recipients, body, html=None, attachments=None):
    """Send email using Flask-Mail."""
    try:
        msg = Message(subject,
                    sender=current_app.config['MAIL_DEFAULT_SENDER'],
                    recipients=recipients)
        msg.body = body
        if html:
            msg.html = html
        if attachments:
            for attachment in attachments:
                msg.attach(*attachment)
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f'Error sending email: {str(e)}')
        return False

def send_appointment_confirmation(appointment):
    """Send appointment confirmation email to patient."""
    subject = 'Appointment Confirmation'
    body = f'''Dear {appointment.patient.first_name},

Your appointment has been scheduled for {appointment.appointment_date.strftime('%B %d, %Y at %I:%M %p')} with Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}.

Please arrive 15 minutes before your scheduled time.

Best regards,
Hospital Management Team'''
    
    return send_email(subject, [appointment.patient.email], body)

def generate_invoice_pdf(bill):
    """Generate PDF invoice for a bill."""
    filename = f'invoice_{bill.id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add hospital header
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    elements.append(Paragraph('Hospital Management System', header_style))
    elements.append(Paragraph(f'Invoice #{bill.id}', styles['Heading2']))
    elements.append(Spacer(1, 20))
    
    # Add patient information
    patient_info = [
        [Paragraph('Patient Name:', styles['Heading4']),
         Paragraph(f'{bill.patient.first_name} {bill.patient.last_name}', styles['Normal'])],
        [Paragraph('Date:', styles['Heading4']),
         Paragraph(bill.bill_date.strftime('%B %d, %Y'), styles['Normal'])],
        [Paragraph('Status:', styles['Heading4']),
         Paragraph(bill.payment_status.title(), styles['Normal'])]
    ]
    
    patient_table = Table(patient_info, colWidths=[100, 400])
    patient_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 20))
    
    # Add bill items
    items_data = [[Paragraph('Description', styles['Heading4']),
                  Paragraph('Quantity', styles['Heading4']),
                  Paragraph('Unit Price', styles['Heading4']),
                  Paragraph('Total', styles['Heading4'])]]
    
    for item in bill.items:
        items_data.append([
            Paragraph(item.description, styles['Normal']),
            Paragraph(str(item.quantity), styles['Normal']),
            Paragraph(f'${item.unit_price:.2f}', styles['Normal']),
            Paragraph(f'${item.total_price:.2f}', styles['Normal'])
        ])
    
    items_table = Table(items_data, colWidths=[250, 75, 100, 75])
    items_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))
    
    # Add total
    total_table = Table([['', Paragraph('Total Amount:', styles['Heading4']),
                         Paragraph(f'${bill.total_amount:.2f}', styles['Heading4'])]],
                       colWidths=[325, 100, 75])
    total_table.setStyle(TableStyle([
        ('ALIGN', (-2, -1), (-1, -1), 'RIGHT'),
        ('TEXTCOLOR', (-2, -1), (-1, -1), colors.black),
        ('FONTSIZE', (-2, -1), (-1, -1), 12),
        ('BOTTOMPADDING', (-2, -1), (-1, -1), 12),
    ]))
    elements.append(total_table)
    
    # Build PDF
    doc.build(elements)
    return filename

def format_currency(amount):
    """Format currency amount."""
    return f'${amount:,.2f}'

def get_current_time_slot(appointment_duration=30):
    """Get available time slots for appointments."""
    now = datetime.now()
    hours = range(9, 18)  # 9 AM to 6 PM
    slots = []
    
    for hour in hours:
        for minute in range(0, 60, appointment_duration):
            time = datetime(now.year, now.month, now.day, hour, minute)
            if time > now:
                slots.append(time)
    
    return slots