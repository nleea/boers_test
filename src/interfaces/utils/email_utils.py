from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings

def send_forget_password_mail(email, token):
    reset_url = f"http://127.0.0.1:8000/auth/change-password/{token}/"
    
    subject = "Password Reset Request"
    
    message = format_html(
        """
        <p>Hi,</p>
        <p>You requested to reset your password. Click the link below to reset it:</p>
        <p><a href='{reset_url}' target='_blank'>{reset_url}</a></p>
        <p>If you prefer, you can copy and paste the following token into the password reset form:</p>
        <p><strong>{token}</strong></p>
        <p>If you did not request this, please ignore this email.</p>
        <p>Best regards,<br>Your Support Team</p>
        """,
        reset_url=reset_url, token=token
    )
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, "", email_from, recipient_list, html_message=message)
    
    return True