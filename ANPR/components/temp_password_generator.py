import secrets
from email.message import EmailMessage
import smtplib
import ssl
from datetime import datetime, timedelta
from django.template.loader import render_to_string
import string


class TempPasswordGenerator:

    def __init__(
            self,
            sender_email='sudaicejeymack@gmail.com',  # os.environ['EMAIL_ADDRESS']
            password='eskg uaxe bvtb miwr'  # os.environ['EMAIL_PASSWORD']
            ):
        self.sender_email = sender_email
        self.password = password

    def temporary_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        secure_password = ''.join(
            secrets.choice(characters) for _ in range(length))
        return secure_password

    def send_temp_email(self, request, receiver_email):
        subject = 'Password Resetting'
        temp_password = self.temporary_password()
        temp_password_expiration_time = datetime.now() + timedelta(minutes=5)
        request.session['sent_temp'] = temp_password
        request.session['temp_expiration_time'] = (
            temp_password_expiration_time.strftime('%Y-%m-%d %H:%M:%S'))

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = receiver_email
        em['Subject'] = 'Password Resetting'

        email_body = render_to_string('temp_passwordemail.html', {
            'subject': subject,
            'temporary_password': temp_password,
            'expiration_time': temp_password_expiration_time.strftime(
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
