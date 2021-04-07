from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_signup_email(name,receiver):
    subject = 'Instagram account created.'
    sender = 'ryandev8121@gmail.com'

    html_content = render_to_string('user/signup-email.html',{"name": name})

    # msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()