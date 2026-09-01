import smtplib
from email.message import EmailMessage
from app.config import settings

def send_email_smtp(recipient_email: str, subject: str, html_body: str):
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"[MAIL MOCK] To: {recipient_email} | Subject: {subject}")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{settings.SENDER_NAME} <{settings.SMTP_USER}>"
        msg["To"] = recipient_email
        msg.set_content("Please enable HTML in your email client to view this message.")
        msg.add_alternative(html_body, subtype="html")

        if int(settings.SMTP_PORT) == 587:
            with smtplib.SMTP(settings.SMTP_HOST, int(settings.SMTP_PORT)) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, int(settings.SMTP_PORT)) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

        print(f"[MAIL SENT] Delivered to {recipient_email}")
    except Exception as e:
        print(f"[MAIL ERROR] Failed sending to {recipient_email}: {e}")

def send_success_email(booking):
    # Formats to: 04-Sep-2026, 02:00 PM
    formatted_start = booking.start_datetime.strftime('%d-%b-%Y, %I:%M %p')
    formatted_end = booking.end_datetime.strftime('%d-%b-%Y, %I:%M %p')

    subject = f"Booking Confirmed: {booking.venue} ({booking.booking_reference[:8]})"
    html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; color: #2d3748; max-width: 600px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #2b6cb0; margin-top: 0;">Venue Reservation Confirmed</h2>
        <p>Dear <strong>{booking.faculty_name}</strong>,</p>
        <p>Your booking request has been approved and logged to the ledger.</p>
        <table style="border-collapse: collapse; width: 100%; margin: 15px 0;">
            <tr><td style="padding: 8px; border: 1px solid #edf2f7; background: #f7fafc; width: 35%;"><strong>Reference ID:</strong></td><td style="padding: 8px; border: 1px solid #edf2f7;">{booking.booking_reference}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #edf2f7; background: #f7fafc;"><strong>Venue:</strong></td><td style="padding: 8px; border: 1px solid #edf2f7;">{booking.venue}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #edf2f7; background: #f7fafc;"><strong>Department:</strong></td><td style="padding: 8px; border: 1px solid #edf2f7;">{booking.department}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #edf2f7; background: #f7fafc;"><strong>Event Purpose:</strong></td><td style="padding: 8px; border: 1px solid #edf2f7;">{booking.event_details}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #edf2f7; background: #f7fafc;"><strong>Start Time:</strong></td><td style="padding: 8px; border: 1px solid #edf2f7;">{formatted_start}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #edf2f7; background: #f7fafc;"><strong>End Time:</strong></td><td style="padding: 8px; border: 1px solid #edf2f7;">{formatted_end}</td></tr>
        </table>
        <p style="font-size: 12px; color: #a0aec0; margin-bottom: 0;">Campus Venue Management System</p>
    </div>
    """
    send_email_smtp(booking.email, subject, html)

def send_clash_email(faculty_name: str, recipient_email: str, venue: str, start_dt, end_dt, clashing_event):
    # Format times nicely for the email body
    req_start = start_dt.strftime('%d-%b-%Y, %I:%M %p')
    req_end = end_dt.strftime('%d-%b-%Y, %I:%M %p')
    clash_start = clashing_event.start_datetime.strftime('%d-%b-%Y, %I:%M %p')
    clash_end = clashing_event.end_datetime.strftime('%I:%M %p')

    subject = f"Booking Request Rejected (Slot Clash): {venue}"
    html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; color: #2d3748; max-width: 600px; border: 1px solid #fed7d7; border-radius: 8px;">
        <h2 style="color: #c53030; margin-top: 0;">Slot Conflict Detected</h2>
        <p>Dear <strong>{faculty_name}</strong>,</p>
        <p>Your booking request for <strong>{venue}</strong> could not be approved due to an overlapping reservation.</p>
        
        <div style="background: #fff5f5; border-left: 4px solid #e53e3e; padding: 12px; margin: 15px 0;">
            <p style="margin: 0 0 6px 0;"><strong>Your Requested Window:</strong><br>{req_start} to {req_end}</p>
            <hr style="border: 0; border-top: 1px solid #fed7d7; margin: 8px 0;">
            <p style="margin: 0;"><strong>Conflicting Reservation:</strong><br>"{clashing_event.event_details}" by <em>{clashing_event.department}</em> ({clash_start} - {clash_end})</p>
        </div>

        <p>Please check the availability calendar and submit a reservation for an alternative slot.</p>
        <p style="font-size: 12px; color: #a0aec0; margin-bottom: 0;">Campus Venue Management System</p>
    </div>
    """
    send_email_smtp(recipient_email, subject, html)