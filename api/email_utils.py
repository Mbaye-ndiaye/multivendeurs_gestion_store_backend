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
        f"Mot de passe temporaire : {plain_password}\n\n"
        "Nous vous recommandons de modifier ce mot de passe lors de votre première connexion.\n\n"
        "Cordialement,\n"
        "L'équipe Gestion Store"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL,
            recipient_list=[vendeur.email],
            fail_silently=False,
        )
        logger.info("Email identifiants envoyé avec succès à %s", vendeur.email)
        return True
    except Exception as e:
        logger.error("Erreur envoi email à %s: %s", vendeur.email, str(e))
        print(f"\n[ERREUR EMAIL] {vendeur.email}: {e}\n")  # Visible dans la console du serveur
        return False
