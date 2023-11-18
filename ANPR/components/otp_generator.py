import secrets
from email.message import EmailMessage
import smtplib
import ssl
from datetime import datetime, timedelta
from django.template.loader import render_to_string


class OTPGenerator:

    def __init__(
            self,
            sender_email='sudaicejeymack@gmail.com',  # os.environ['EMAIL_ADDRESS']
            password='eskg uaxe bvtb miwr'  # os.environ['EMAIL_PASSWORD']
            ):
        self.sender_email = sender_email
        self.password = password

    def generate_otp(self, length=6):
        otp = ''.join(secrets.choice('0123456789') for _ in range(length))
        return otp

    def send_otp_email(self, request, receiver_email):
        subject = 'Account Verification'
        otp = self.generate_otp()
        otp_expiration_time = datetime.now() + timedelta(minutes=5)
        request.session['sent_otp'] = otp
        request.session['expiration_time'] = otp_expiration_time.strftime(
            '%Y-%m-%d %H:%M:%S')

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = receiver_email
        em['Subject'] = 'Login Confirmation'

        email_body = render_to_string('otpemail.html', {
            'subject': subject,
            'otp': otp,
            'expiration_time': otp_expiration_time.strftime(
                '%Y-%m-%d %H:%M:%S')
        })

        em.set_content(f'', subtype='html')
        em.add_alternative(email_body, subtype='html')
        context = ssl.create_default_context()

        try:
            with (
                smtplib.SMTP_SSL(
                    'smtp.gmail.com', 465, context=context
                    )
                    as smtp
            ):
                smtp.login(self.sender_email, self.password)
                smtp.sendmail(
                    self.sender_email,
                    receiver_email,
                    em.as_string())
                print(f'OTP email sent successfully to {receiver_email}.')
        except Exception as e:
            print(f'Error sending OTP email: {str(e)}')
