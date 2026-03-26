"""
Envoi d'emails (identifiants vendeur, etc.).
"""
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_vendeur_credentials(vendeur, plain_password):
    """
    Envoie au vendeur un email avec ses identifiants de connexion (email + mot de passe).
    Retourne True si l'envoi a réussi, False sinon.
    """
    subject = "Vos identifiants - Espace vendeur"
    message = (
        f"Bonjour {vendeur.prenom or ''} {vendeur.nom or ''},\n\n"
        "Votre compte vendeur a été créé. Voici vos identifiants de connexion :\n\n"
        f"Email (identifiant) : {vendeur.email}\n"
        f"Mot de passe : {plain_password}\n\n"
        "Nous vous recommandons de modifier ce mot de passe lors de votre première connexion.\n\n"
        "Cordialement,\n"
        "L'équipe Gestion Store"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[vendeur.email],
            fail_silently=False,
        )
        logger.info("Email identifiants envoyé avec succès à %s", vendeur.email)
        return True
    except Exception as e:
        logger.error("Erreur envoi email à %s: %s", vendeur.email, str(e))
        print(f"\n[ERREUR EMAIL] {vendeur.email}: {e}\n")  # Visible dans la console du serveur
        return False


def send_otp_email(user, code):
    """
    Envoie le code OTP par email après une tentative de connexion réussie (email + mot de passe).
    Retourne True si l'envoi a réussi, False sinon.
    """
    app_name = getattr(settings, 'APP_NAME', None) or 'Gestion Store'
    subject = f"Votre code de vérification - {app_name}"
    message = (
        f"Bonjour {user.prenom or ''} {user.nom or ''},\n\n"
        f"Votre code de vérification pour terminer la connexion est : {code}\n\n"
        "Ce code est valide 5 minutes. Ne le partagez avec personne.\n\n"
        "Cordialement,\n"
        f"L'équipe {app_name}"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER or getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info("OTP envoyé avec succès à %s", user.email)
        return True
    except Exception as e:
        logger.error("Erreur envoi OTP à %s: %s", user.email, str(e))
        print(f"\n[ERREUR EMAIL OTP] {user.email}: {e}\n")
        return False


def send_password_reset_email(user, reset_token):
    """
    Envoie un email avec le lien/token de réinitialisation de mot de passe.
    Retourne True si l'envoi a réussi, False sinon.
    """
    app_name = getattr(settings, 'APP_NAME', None) or 'Gestion Store'
    subject = f"Réinitialisation de votre mot de passe - {app_name}"
    reset_url = f"http://localhost:8000/dashboard/reset-password/{reset_token}/"  # À adapter selon ton frontend

    message = (
        f"Bonjour {user.prenom or ''} {user.nom or ''},\n\n"
        "Vous avez demandé la réinitialisation de votre mot de passe.\n\n"
        f"Voici votre token de réinitialisation : {reset_token}\n\n"
        f"Ou cliquez sur ce lien pour réinitialiser votre mot de passe :\n{reset_url}\n\n"
        "Ce token est valide 1 heure. Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.\n\n"
        "Cordialement,\n"
        f"L'équipe {app_name}"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info("Email de reset envoyé avec succès à %s", user.email)
        return True
    except Exception as e:
        logger.error("Erreur envoi email reset à %s: %s", user.email, str(e))
        print(f"\n[ERREUR EMAIL RESET] {user.email}: {e}\n")
        return False
