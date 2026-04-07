from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from mimetypes import MimeTypes
import logging

logger = logging.getLogger(__name__)



APP_NAME = getattr(settings, 'APP_NAME', 'Gestion-Stock')

def send_email(subject, to, template_src, context_dict=None, file=None):
    """
    Envoie un email HTML au destinataire.

    Args:
        subject: Sujet de l'email
        to: Adresse email du destinataire (str)
        template_src: Chemin du template HTML (ex: 'mail_notification.html')
        context_dict: Dictionnaire de contexte pour le template
        file: Fichier à joindre (optionnel)
    """
    if context_dict is None:
        context_dict = {}

    try:
        # Même logique que backend_easymarket_multivendor (Notif.send_email)
        if hasattr(settings, 'EMAIL_HOST_USER') and getattr(settings, 'EMAIL_HOST_PASSWORD', None):
            from_email = f'{APP_NAME} <{settings.EMAIL_HOST_USER}>'
        else:
            from_email = f'{APP_NAME} <noreply@babacarndiay546.com>'
            logger.warning("EMAIL_HOST_USER ou EMAIL_HOST_PASSWORD non configuré. Email peut échouer.")

        html_content = render_to_string(template_src, context_dict)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [to],
        )

        if file:
            msg.attach(file.name, file.read(), file.content_type if hasattr(file, 'content_type') else 'application/octet-stream')

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(f"Email envoyé avec succès à {to}")
        return True

    except Exception as e:
        logger.error(f"Erreur envoi email à {to}: {str(e)}")
        return False


class Notif:
    """
    Version alignée sur backend_easymarket_multivendor:
    Notif.send_email(APP_NAMES, subject, to, template_src, context_dict, file)
    """

    def send_email(APP_NAMES, subject, to, template_src, context_dict=None, file=None):
        if context_dict is None:
            context_dict = {}
        try:
            if hasattr(settings, 'EMAIL_HOST_USER') and getattr(settings, 'EMAIL_HOST_PASSWORD', None):
                connection = None
                from_email = f'{APP_NAMES} <{settings.EMAIL_HOST_USER}>'
            else:
                connection = None
                from_email = f'{APP_NAMES} <noreply@babacarndiay546.com>'

            html_content = render_to_string(template_src, context_dict)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to], connection=connection)

            if file:
                mime = MimeTypes()
                file_type = mime.guess_type(file.url if hasattr(file, "url") else "")
                content_type = file_type[0] if file_type and file_type[0] else 'application/octet-stream'
                msg.attach(file.name, file.read(), content_type)

            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info(f"Email envoyé avec succès à {to}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi email à {to}: {str(e)}")
            return False

    def send_email_to_many(APP_NAMES, subject, emails, template_src, context_dict=None, file=None):
        if context_dict is None:
            context_dict = {}
        try:
            if hasattr(settings, 'EMAIL_HOST_USER') and getattr(settings, 'EMAIL_HOST_PASSWORD', None):
                connection = None
                from_email = f'{APP_NAMES} <{settings.EMAIL_HOST_USER}>'
            else:
                connection = None
                from_email = f'{APP_NAMES} <noreply@babacarndiay546.com>'

            html_content = render_to_string(template_src, context_dict)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, list(emails), connection=connection)

            if file:
                mime = MimeTypes()
                file_type = mime.guess_type(file.url if hasattr(file, "url") else "")
                content_type = file_type[0] if file_type and file_type[0] else 'application/octet-stream'
                msg.attach(file.name, file.read(), content_type)

            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info(f"Emails envoyés avec succès à {len(emails)} destinataires")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi emails à {emails}: {str(e)}")
            return False

    def notify_admins(admins, subject, template_src, context_dict):
        for admin in admins:
            context_dict["admin"] = admin
            Notif.send_email(APP_NAME, subject, admin.email, template_src, context_dict=context_dict)
