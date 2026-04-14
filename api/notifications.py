# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from mimetypes import MimeTypes
from django.utils.html import strip_tags
from django.conf import settings
import requests
import json
import logging


# Configuration du logger
logger = logging.getLogger(__name__)

# Ne pas créer la connexion au niveau du module pour éviter les problèmes de configuration
FROM_EMAIL = None

# Récupérer APP_NAME depuis les settings
try:
    APP_NAME = settings.APP_NAME
except:
    APP_NAME = "GESTION STOCK"


class Notif():

    # def push_notif(to, title, body, data):
    #     print(f"🔔 === DÉBUT NOTIFICATION PUSH ===")
    #     print(f"📱 To: {to}")
    #     print(f"📋 Title: {title}")
    #     print(f"📄 Body: {body}")
    #     print(f"📊 Data: {data}")

    #     # Vérifier si le token est valide
    #     if not to or to == "" or to == []:
    #         print("❌ ERREUR - Token vide ou invalide")
    #         logger.error(f"Token de notification invalide: {to}")
    #         return

    #     # Si c'est une liste, traiter chaque token
    #     if isinstance(to, list):
    #         print(f"📋 Envoi à {len(to)} destinataires")
    #         for i, token in enumerate(to):
    #             print(f"   [{i+1}/{len(to)}] Envoi à: {token[:20]}...")
    #             Notif._send_single_push_notif(token, title, body, data)
    #     else:
    #         # Token unique
    #         Notif._send_single_push_notif(to, title, body, data)

    # def _send_single_push_notif(token, title, body, data):
    #     """Envoie une notification push à un seul token"""
    #     print(f"📤 Envoi notification push à: {token[:20]}...")

    #     message = {
    #         "to": token,
    #         "sound": "default",
    #         "title": title,
    #         "body": body,
    #         "data": data
    #     }

    #     try:
    #         print(f"🌐 Envoi vers Expo...")
    #         response = requests.post(
    #             "https://exp.host/--/api/v2/push/send",
    #             headers={
    #                 "Accept": "application/json",
    #                 "Accept-encoding": "gzip, deflate",
    #                 "Content-Type": "application/json"
    #             },
    #             data=json.dumps(message),
    #             timeout=30
    #         )

    #         print(f"✅ Réponse Expo: {response.status_code}")
    #         if response.status_code == 200:
    #             result = response.json()
    #             print(f"📊 Résultat: {result}")
    #             if 'data' in result and result['data'].get('status') == 'error':
    #                 print(
    #                     f"❌ Erreur Expo: {result['data'].get('message', 'Erreur inconnue')}")
    #                 logger.error(
    #                     f"Erreur Expo pour token {token[:20]}...: {result['data']}")
    #             else:
    #                 print(f"✅ Notification envoyée avec succès")
    #                 logger.info(
    #                     f"Notification push envoyée avec succès à {token[:20]}...")
    #         else:
    #             print(
    #                 f"❌ Erreur HTTP: {response.status_code} - {response.text}")
    #             logger.error(
    #                 f"Erreur HTTP {response.status_code} pour token {token[:20]}...: {response.text}")

    #     except requests.exceptions.Timeout:
    #         print(f"⏰ Timeout lors de l'envoi à {token[:20]}...")
    #         logger.error(
    #             f"Timeout lors de l'envoi de notification push à {token[:20]}...")
    #     except requests.exceptions.RequestException as e:
    #         print(
    #             f"❌ Erreur réseau lors de l'envoi à {token[:20]}...: {str(e)}")
    #         logger.error(f"Erreur réseau pour token {token[:20]}...: {str(e)}")
    #     except Exception as e:
    #         print(
    #             f"❌ Erreur inattendue lors de l'envoi à {token[:20]}...: {str(e)}")
    #         logger.error(
    #             f"Erreur inattendue pour token {token[:20]}...: {str(e)}")

    def send_email(APP_NAMES, subject, to, template_src, context_dict={}, file=None):
        print(f"📧 === DÉBUT ENVOI EMAIL ===")
        print(f"📨 To: {to}")
        print(f"📋 Subject: {subject}")
        print(f"📄 Template: {template_src}")

        try:
            # Configuration email conditionnelle
            if hasattr(settings, 'EMAIL_HOST_USER') and hasattr(settings, 'EMAIL_HOST_PASSWORD'):
                # Utiliser la configuration par défaut de Django
                connection = None  # Laisser Django utiliser les settings par défaut
                from_email = f'{APP_NAMES} <{settings.EMAIL_HOST_USER}>'
            else:
                # En mode DEBUG, utiliser le backend console
                connection = None
                from_email = f'{APP_NAMES} <noreply@babacarndiay546.com>'
            print(f"📤 From: {from_email}")

            if file:
                mime = MimeTypes()
                file_type = mime.guess_type(file.url)
                # render with dynamic value
                html_content = render_to_string(template_src, context_dict)
                # Strip the html tag. So people can see the pure text at least.
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email,
                                             [to], connection=connection)
                msg.attach(file.name, file.read(), file_type[0])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            else:
                # render with dynamic value
                html_content = render_to_string(template_src, context_dict)
                # Strip the html tag. So people can see the pure text at least.
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email,
                                             [to], connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            print(f"✅ Email envoyé avec succès à {to}")
            logger.info(f"Email envoyé avec succès à {to}")

        except Exception as e:
            print(f"❌ Erreur envoi email: {str(e)}")
            logger.error(f"Erreur envoi email à {to}: {str(e)}")
            # Ne pas faire échouer le processus principal
            pass

    def send_email_to_many(APP_NAMES, subject, emails, template_src, context_dict={},
                           file=None):
        print(f"📧 === DÉBUT ENVOI EMAILS MULTIPLES ===")
        print(f"📨 To: {emails}")
        print(f"📋 Subject: {subject}")
        print(f"📄 Template: {template_src}")

        try:
            # Configuration email conditionnelle
            if hasattr(settings, 'EMAIL_HOST_USER') and hasattr(settings, 'EMAIL_HOST_PASSWORD'):
                # Utiliser la configuration par défaut de Django
                connection = None  # Laisser Django utiliser les settings par défaut
                from_email = f'{APP_NAMES} <{settings.EMAIL_HOST_USER}>'
            else:
                # En mode DEBUG, utiliser le backend console
                connection = None
                from_email = f'{APP_NAMES} <noreply@babacarndiay546.com>'
            print(f"📤 From: {from_email}")

            if file:
                mime = MimeTypes()
                file_type = mime.guess_type(file.url)
                # render with dynamic value
                html_content = render_to_string(template_src, context_dict)
                # Strip the html tag. So people can see the pure text at least.
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email,
                                             list(emails), connection=connection)
                msg.attach(file.name, file.read(), file_type[0])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            else:
                # render with dynamic value
                html_content = render_to_string(template_src, context_dict)
                # Strip the html tag. So people can see the pure text at least.
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email,
                                             list(emails), connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            print(
                f"✅ Emails envoyés avec succès à {len(emails)} destinataires")
            logger.info(
                f"Emails envoyés avec succès à {len(emails)} destinataires")

        except Exception as e:
            print(f"❌ Erreur envoi emails: {str(e)}")
            logger.error(f"Erreur envoi emails à {emails}: {str(e)}")
            # Ne pas faire échouer le processus principal
            pass

    def notify_admins(admins, subject, template_src, context_dict):
        print(f"👥 === NOTIFICATION ADMINS ===")
        print(f"👤 Nombre d'admins: {len(admins)}")
        print(f"📋 Subject: {subject}")

        for i, admin in enumerate(admins):
            print(f"📧 [{i+1}/{len(admins)}] Envoi à admin: {admin.email}")
            context_dict["admin"] = admin
            Notif.send_email("GESTION STOCK", subject, admin.email,
                             template_src, context_dict=context_dict)
