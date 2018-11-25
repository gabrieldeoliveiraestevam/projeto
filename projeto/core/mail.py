# Realiza a organização do email
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_mail_template(subject, template_name, context, recipient_list, 
    from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False, files=None):

	# Faz a redenrização do template e gera string
    message_html = render_to_string(template_name, context)

    # Filtra message_html retirando as tags
    message_txt = striptags(message_html)
    
    # Formatação alternativa de email
    email = EmailMultiAlternatives(
        subject=subject, body=message_txt, from_email=from_email, 
        bbc=recipient_list
    )

    # Verifica se arquivo foi informado
    if files:
        email.attach(files.name, files.read(), files.content_type) # Anexa arquivo

    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently) # Envia email e verifica falha no envio

