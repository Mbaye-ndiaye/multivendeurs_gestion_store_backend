# -*- coding: utf-8 -*-
"""
Module de notifications par email.
Utilise Django EmailMultiAlternatives pour l'envoi d'emails HTML.
"""
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


# Aligné sur backend_easymarket_multivendor : APP_NAME depuis settings
APP_NAME = getattr(settings, 'APP_NAME', 'Gestio-Stock')


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
            from_email = f'{APP_NAME} <noreply@gestio-stock.local>'
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
