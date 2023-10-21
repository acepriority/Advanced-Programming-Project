import secrets
from email.message import EmailMessage
import smtplib
import ssl
from datetime import datetime, timedelta
from django.template.loader import render_to_string


def generate_otp(length=6):
    otp = ''.join(secrets.choice('0123456789') for _ in range(length))
    return otp


sender_email = 'sudaicejeymack@gmail.com'
password = 'eskg uaxe bvtb miwr'
receiver_email = 'mukwayamels@gmail.com'


subject = 'Account Verification'
otp = generate_otp()
otp_expiration_time = datetime.now() + timedelta(minutes=5)


em = EmailMessage()
em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = 'Password Resetting'

email_body = render_to_string('otpemail.html', {
    'subject': subject,
    'otp': otp,
    'expiration_time': otp_expiration_time.strftime('%Y-%m-%d %H:%M:%S')
})

em.set_content(f'', subtype='html')
em.add_alternative(email_body, subtype='html')
context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())
        print(f'OTP email sent successfully to {receiver_email}.')
except Exception as e:
    print(f'Error sending OTP email: {str(e)}')
