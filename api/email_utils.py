# """
# Envoi d'emails (identifiants vendeur, etc.).
# """
# import logging
# from django.core.mail import send_mail
# from django.conf import settings
# from django.http import HttpResponse

# # from backend.settings import EMAIL_HOST_USER
# from django.core.mail import EmailMultiAlternatives
# from mimetypes import MimeTypes
# from django.utils.html import strip_tags
# from django.template.loader import render_to_string

# logger = logging.getLogger(__name__)


# def send_vendeur_credentials(vendeur, plain_password):
#     """
#     Envoie au vendeur un email avec ses identifiants de connexion (email + mot de passe).
#     Retourne True si l'envoi a réussi, False sinon.
#     """
#     subject = "Vos identifiants - Espace vendeur"
#     message = (
#         f"Bonjour {vendeur.prenom or ''} {vendeur.nom or ''},\n\n"
#         "Votre compte vendeur a été créé. Voici vos identifiants de connexion :\n\n"
#         f"Email (identifiant) : {vendeur.email}\n"
#         f"Mot de passe : {plain_password}\n\n"
#         "Nous vous recommandons de modifier ce mot de passe lors de votre première connexion.\n\n"
#         "Cordialement,\n"
#         "L'équipe Gestion Store"
#     )
#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[vendeur.email],
#             fail_silently=False,
#         )
#         logger.info("Email identifiants envoyé avec succès à %s", vendeur.email)
#         return True
#     except Exception as e:
#         logger.error("Erreur envoi email à %s: %s", vendeur.email, str(e))
#         print(f"\n[ERREUR EMAIL] {vendeur.email}: {e}\n")  # Visible dans la console du serveur
#         return False
#     # def test_email(request):
#     #     send_mail(
#     #     "Test",
#     #     "Email fonctionne",
#     #     EMAIL_HOST_USER,
#     #     ["babacarndiay546@gmail.com"],
#     #     fail_silently=False
#     # )
#     # return HttpResponse("Email envoyé")

# def send_email(APP_NAMES, subject, to, template_src, context_dict={}, file=None):
#         print(f"📧 === DÉBUT ENVOI EMAIL ===")
#         print(f"📨 To: {to}")
#         print(f"📋 Subject: {subject}")
#         print(f"📄 Template: {template_src}")

#         try:
#             # Configuration email conditionnelle
#             if hasattr(settings, 'EMAIL_HOST_USER') and hasattr(settings, 'EMAIL_HOST_PASSWORD'):
#                 # Utiliser la configuration par défaut de Django
#                 connection = None  # Laisser Django utiliser les settings par défaut
#                 from_email = f'{APP_NAMES} <{settings.EMAIL_HOST_USER}>'
#             else:
#                 # En mode DEBUG, utiliser le backend console
#                 connection = None
#                 from_email = f'{APP_NAMES} <noreply@gestionstock.com>'
#             print(f"📤 From: {from_email}")

#             if file:
#                 mime = MimeTypes()
#                 file_type = mime.guess_type(file.url)
#                 # render with dynamic value
#                 html_content = render_to_string(template_src, context_dict)
#                 # Strip the html tag. So people can see the pure text at least.
#                 text_content = strip_tags(html_content)
#                 msg = EmailMultiAlternatives(subject, text_content, from_email,
#                                              [to], connection=connection)
#                 msg.attach(file.name, file.read(), file_type[0])
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()
#             else:
#                 # render with dynamic value
#                 html_content = render_to_string(template_src, context_dict)
#                 # Strip the html tag. So people can see the pure text at least.
#                 text_content = strip_tags(html_content)
#                 msg = EmailMultiAlternatives(subject, text_content, from_email,
#                                              [to], connection=connection)
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()

#             print(f"✅ Email envoyé avec succès à {to}")
#             logger.info(f"Email envoyé avec succès à {to}")

#         except Exception as e:
#             print(f"❌ Erreur envoi email: {str(e)}")
#             logger.error(f"Erreur envoi email à {to}: {str(e)}")
#             # Ne pas faire échouer le processus principal
#             pass


# def send_otp_email(user, code):
#     """
#     Envoie le code OTP par email après une tentative de connexion réussie (email + mot de passe).
#     Retourne True si l'envoi a réussi, False sinon.
#     """
#     app_name = getattr(settings, 'APP_NAME', None) or 'Gestion Store'
#     subject = f"Votre code de vérification - {app_name}"
#     message = (
#         f"Bonjour {user.prenom or ''} {user.nom or ''},\n\n"
#         f"Votre code de vérification pour terminer la connexion est : {code}\n\n"
#         "Ce code est valide 5 minutes. Ne le partagez avec personne.\n\n"
#         "Cordialement,\n"
#         f"L'équipe {app_name}"
#     )
#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER or getattr(settings, 'DEFAULT_FROM_EMAIL', None),
#             recipient_list=[user.email],
#             fail_silently=False,
#         )
#         logger.info("OTP envoyé avec succès à %s", user.email)
#         return True
#     except Exception as e:
#         logger.error("Erreur envoi OTP à %s: %s", user.email, str(e))
#         print(f"\n[ERREUR EMAIL OTP] {user.email}: {e}\n")
#         return False


# def send_password_reset_email(user, reset_token):
#     """
#     Envoie un email avec le lien/token de réinitialisation de mot de passe.
#     Retourne True si l'envoi a réussi, False sinon.
#     """
#     app_name = getattr(settings, 'APP_NAME', None) or 'Gestion Store'
#     subject = f"Réinitialisation de votre mot de passe - {app_name}"
#     reset_url = f"http://localhost:8000/dashboard/reset-password/{reset_token}/"  # À adapter selon ton frontend

#     message = (
#         f"Bonjour {user.prenom or ''} {user.nom or ''},\n\n"
#         "Vous avez demandé la réinitialisation de votre mot de passe.\n\n"
#         f"Voici votre token de réinitialisation : {reset_token}\n\n"
#         f"Ou cliquez sur ce lien pour réinitialiser votre mot de passe :\n{reset_url}\n\n"
#         "Ce token est valide 1 heure. Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.\n\n"
#         "Cordialement,\n"
#         f"L'équipe {app_name}"
#     )
#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email],
#             fail_silently=False,
#         )
#         logger.info("Email de reset envoyé avec succès à %s", user.email)
#         return True
#     except Exception as e:
#         logger.error("Erreur envoi email reset à %s: %s", user.email, str(e))
#         print(f"\n[ERREUR EMAIL RESET] {user.email}: {e}\n")
#         return False


"""
Implémentation active (l'ancien code est conservé en commentaires ci-dessus).
Configuration alignée avec backend_easymarket_multivendor.
"""
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_vendeur_credentials(vendeur, plain_password):
    subject = "Vos identifiants - Espace vendeur"
    app_name = getattr(settings, 'APP_NAME', 'EASY MARKET')
    message = (
        f"Bonjour {vendeur.prenom or ''} {vendeur.nom or ''},\n\n"
        "Votre compte vendeur a ete cree. Voici vos identifiants de connexion :\n\n"
        f"Email (identifiant) : {vendeur.email}\n"
        f"Mot de passe temporaire : {plain_password}\n\n"
        "Nous vous recommandons de modifier ce mot de passe lors de votre premiere connexion.\n\n"
        "Cordialement,\n"
        f"L'equipe {app_name}"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER or f"noreply@{app_name.lower().replace(' ', '')}.com",
            recipient_list=[vendeur.email],
            fail_silently=False,
        )
        logger.info("Email identifiants envoye avec succes a %s", vendeur.email)
        return True
    except Exception as e:
        logger.error("Erreur envoi email a %s: %s", vendeur.email, str(e))
        return False


def send_otp_email(user, code):
    app_name = getattr(settings, 'APP_NAME', None) or 'EASY MARKET'
    subject = f"Votre code de verification - {app_name}"
    message = (
        f"Bonjour {user.prenom or ''} {user.nom or ''},\n\n"
        f"Votre code de verification pour terminer la connexion est : {code}\n\n"
        "Ce code est valide 5 minutes. Ne le partagez avec personne.\n\n"
        "Cordialement,\n"
        f"L'equipe {app_name}"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER or getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info("OTP envoye avec succes a %s", user.email)
        return True
    except Exception as e:
        logger.error("Erreur envoi OTP a %s: %s", user.email, str(e))
        return False


def send_password_reset_email(user, reset_token):
    app_name = getattr(settings, 'APP_NAME', None) or 'EASY MARKET'
    subject = f"Reinitialisation de votre mot de passe - {app_name}"
    reset_url = f"http://localhost:8000/dashboard/reset-password/{reset_token}/"
    message = (
        f"Bonjour {user.prenom or ''} {user.nom or ''},\n\n"
        "Vous avez demande la reinitialisation de votre mot de passe.\n\n"
        f"Voici votre token de reinitialisation : {reset_token}\n\n"
        f"Ou cliquez sur ce lien pour reinitialiser votre mot de passe :\n{reset_url}\n\n"
        "Ce token est valide 1 heure. Si vous n'avez pas demande cette reinitialisation, ignorez cet email.\n\n"
        "Cordialement,\n"
        f"L'equipe {app_name}"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info("Email de reset envoye avec succes a %s", user.email)
        return True
    except Exception as e:
        logger.error("Erreur envoi email reset a %s: %s", user.email, str(e))
        return False
