"""
Commande pour tester la configuration email.
Usage: python manage.py test_email
       python manage.py test_email kheud@gmail.com
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Teste l'envoi d'email et affiche la configuration actuelle"

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            nargs='?',
            default='test@example.com',
            help='Adresse email de destination pour le test',
        )

    def handle(self, *args, **options):
        to_email = options['email']

        # Afficher la configuration
        self.stdout.write("\n=== Configuration Email actuelle ===\n")
        self.stdout.write(f"  EMAIL_BACKEND   : {getattr(settings, 'EMAIL_BACKEND', 'N/A')}")
        self.stdout.write(f"  EMAIL_HOST      : {getattr(settings, 'EMAIL_HOST', 'N/A')}")
        self.stdout.write(f"  EMAIL_PORT      : {getattr(settings, 'EMAIL_PORT', 'N/A')}")
        self.stdout.write(f"  EMAIL_HOST_USER : {getattr(settings, 'EMAIL_HOST_USER', 'N/A') or '(vide)'}")
        pwd = getattr(settings, 'EMAIL_HOST_PASSWORD', '') or ''
        pwd_display = f"{pwd[:4]}****{pwd[-2:]}" if len(pwd) > 6 else "(vide ou trop court)"
        self.stdout.write(f"  EMAIL_HOST_PASS : {pwd_display}\n")

        # Vérifier si configuré
        if not getattr(settings, 'EMAIL_HOST_USER', None) or not getattr(settings, 'EMAIL_HOST_PASSWORD', None):
            self.stdout.write(self.style.ERROR(
                "ERREUR: EMAIL_HOST_USER ou EMAIL_HOST_PASSWORD manquant dans .env"
            ))
            self.stdout.write("Ajoutez-les dans votre fichier .env\n")
            return

        # Essayer d'envoyer
        self.stdout.write(f"Envoi d'un email test à {to_email}...\n")
        try:
            send_mail(
                subject="Test email Gestio-Stock",
                message="Ceci est un email de test. Si vous le recevez, la config email fonctionne.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS("[OK] Email envoye avec succes !"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERREUR] {e}"))
            self.stdout.write("\nSolutions possibles:")
            self.stdout.write("  1. Gmail: Utilisez un MOT DE PASSE D'APPLICATION (pas le mot de passe du compte)")
            self.stdout.write("     → https://myaccount.google.com/apppasswords")
            self.stdout.write("  2. Ou utilisez Mailtrap (gratuit) pour tester:")
            self.stdout.write("     → Créez un compte sur https://mailtrap.io")
            self.stdout.write("     → Dans .env : EMAIL_HOST=smtp.mailtrap.io EMAIL_PORT=2525")
            self.stdout.write("     → Et les identifiants Mailtrap pour USER/PASSWORD\n")
