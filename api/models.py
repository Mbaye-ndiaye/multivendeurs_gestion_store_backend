from django.db import models
from django.utils import timezone
import datetime
import uuid
from django.db.models import JSONField
from safedelete.config import DELETED_INVISIBLE
from safedelete.managers import SafeDeleteManager
from safedelete.models import SafeDeleteModel
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import secrets
import hashlib
from django.db.models import Sum
import decimal
# from api.utils import Utils  # TODO: Créer le fichier utils.py si nécessaire
from rest_framework import serializers
from decimal import Decimal



ACHETEUR = 'ACHETEUR'
VENDEUR = 'VENDEUR'
DELETED = 'DELETED'
ADMIN = 'admin'
SUPERADMIN = 'superadmin'
USER_TYPES = (
    (ADMIN, ADMIN),
    (SUPERADMIN, SUPERADMIN),
    (VENDEUR, VENDEUR),
    (ACHETEUR, ACHETEUR),
    (DELETED, DELETED),
)





EUR = 'EUR'
USD = 'USD'
XOF = 'XOF'
CURRENCY = (
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('XOF', 'XOF')
)

# --- Champs optionnels vendeur (décommenter quand besoin) ---
# TMONEY = 'TMONEY'
# FLOOZ = 'FLOOZ'
# PAYGATE_NETWORK = (
#     (TMONEY, TMONEY),
#     (FLOOZ, FLOOZ),
# )

# EMAIL = 'EMAIL'
# SMS = 'SMS'
# AUTRE = 'AUTRE'
# SERVICES = (
#     (EMAIL, EMAIL),
#     (SMS, SMS),
#     (AUTRE, AUTRE)
# )

ADMIN_TYPE = (
    (ADMIN, ADMIN),
    (SUPERADMIN, SUPERADMIN)
)

FACTURE_PAYEE = 'payée'
FACTURE_NON_PAYEE = 'non payée'
FACTURE_PARTIELLEMENT = 'partiellement payée'
FACTURE_PAID_STATUT = (
    (FACTURE_PAYEE, FACTURE_PAYEE),
    (FACTURE_NON_PAYEE, FACTURE_NON_PAYEE),
    (FACTURE_PARTIELLEMENT, FACTURE_PARTIELLEMENT),
)


def _date_aujourdhui():
    return timezone.now().date()

TAILLE_UNIQUE = "taille_unique"
TAILLE_VARIABLE = "taille_variable"
TAILLE_UNIQUE_AVEC_COULEUR = "taille_unique_avec_couleur"
TYPE_ARTICLES = (
    (TAILLE_UNIQUE, TAILLE_UNIQUE),
    (TAILLE_VARIABLE, TAILLE_VARIABLE),
    (TAILLE_UNIQUE_AVEC_COULEUR, TAILLE_UNIQUE_AVEC_COULEUR),
)

class MyModelManager(SafeDeleteManager):
    _safedelete_visibility = DELETED_INVISIBLE


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', SUPERADMIN)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    slug = models.SlugField(default=uuid.uuid1)
    nom = models.CharField(max_length=1000, blank=True, null=True)
    token = models.CharField(max_length=1000, blank=True, null=True)
    # tokens = models.JSONField(default=[], blank=True)
    tokens = models.JSONField(default=list, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    prenom = models.CharField(max_length=1000, blank=True, null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=30, unique=True)
    adresse = models.CharField(max_length=255, null=True)
    pays = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_archive = models.BooleanField(default=False)
    deletion_id = models.CharField(max_length=1000, blank=True, null=True)
    deletion_type = models.CharField(
        max_length=50, choices=USER_TYPES, blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    deleted_by_cascade = models.CharField(
        null=True, blank=True, max_length=1000)
    register_by_social_media = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    signature = models.ImageField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # these field are required on registering
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        app_label = "api"

    def __str__(self):
        return f'<User: {self.pk},email: {self.email}, telephone: {self.telephone}, ,user_type: {self.user_type}>'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)


class AdminUser(User):
    admin_type = models.CharField(
        max_length=20, choices=ADMIN_TYPE, default=ADMIN)
    def __str__(self):
        return str(self.email)

class Vendeur(User):
    """
    Modèle Vendeur héritant de User.
    Permet d'avoir un système d'authentification complet pour les vendeurs.
    """
    nom_de_la_boutique = models.CharField(max_length=200)
    # couleur = models.CharField(max_length=50, blank=True, null=True)
    domaine = models.CharField(max_length=200, blank=True, null=True)
    devise = models.CharField(max_length=20, choices=CURRENCY, default=XOF)

    # ---------- Champs à décommenter quand vous en avez besoin ----------
    # api_key (hashée en base, générée au save si vide)
    # api_key = models.CharField(max_length=200, blank=True, null=True)
    #
    # devise (déjà actif ci-dessus ; décommenter la ligne ci-dessous si vous le déplacez ici)
    # devise = models.CharField(max_length=20, choices=CURRENCY, default=XOF)
    #
    # Stripe
    # stripe_publishable_key = models.CharField(max_length=200, null=True, blank=True)
    # stripe_secret_key = models.CharField(max_length=200, null=True, blank=True)
    # stripe_is_set = models.BooleanField(default=False)
    # stripe_endpoint_secret = models.CharField(max_length=200, null=True, blank=True)
    #
    # Paygate (décommenter aussi PAYGATE_NETWORK en haut du fichier)
    # paygate_api_key = models.CharField(max_length=200, null=True, blank=True)
    # paygate_is_set = models.BooleanField(default=False)
    # paygate_network = models.CharField(max_length=50, choices=PAYGATE_NETWORK, default=TMONEY)
    # --------------------------------------------------------------------

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "Vendeur"
        verbose_name_plural = "Vendeurs"
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.nom_de_la_boutique)

    def save(self, *args, **kwargs):
        # Définir le type d'utilisateur comme VENDEUR
        if not self.user_type:
            self.user_type = VENDEUR

        # Générer et hasher la clé API si besoin (décommenter quand api_key est activé)
        # if not self.api_key:
        #     api_key = secrets.token_hex(32)  # 32 bytes = 64 caractères
        #     hashed_api_key = hashlib.sha256(api_key.encode()).hexdigest()
        #     self.api_key = hashed_api_key

        super().save(*args, **kwargs)


class LoginOTP(models.Model):
    """
    Code OTP envoyé par email après un login réussi (email + mot de passe).
    Permet de finaliser l'authentification via POST /api/verify-otp/.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "OTP de connexion"
        verbose_name_plural = "OTP de connexion"
        ordering = ("-created_at",)

    def __str__(self):
        return f"OTP user={self.user_id} exp={self.expires_at}"

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at


class PasswordResetToken(models.Model):
    """
    Token de réinitialisation de mot de passe envoyé par email.
    Permet de réinitialiser le mot de passe via POST /api/reset-password/.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Token de reset mot de passe"
        verbose_name_plural = "Tokens de reset mot de passe"
        ordering = ("-created_at",)

    def __str__(self):
        return f"Reset token user={self.user_id} exp={self.expires_at}"

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at


class Facture(models.Model):
    """
    Facture émise par un vendeur : en-tête client + référence, total, lignes détaillées.
    La signature du vendeur est l'image `User.signature` (héritée par Vendeur).
    PDF généré comme Easymarket (template facturation.html + WeasyPrint).
    """
    slug = models.SlugField(default=uuid.uuid1)
    reference = models.CharField(max_length=100)
    client_nom = models.CharField(max_length=500)
    client_telephone = models.CharField(max_length=50)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE, related_name='factures')
    total_general = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    date_facture = models.DateField(default=_date_aujourdhui)
    date_echeance = models.DateField(default=_date_aujourdhui)
    remise = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    paid_statut = models.CharField(
        max_length=40, choices=FACTURE_PAID_STATUT, default=FACTURE_NON_PAYEE)
    facture_pdf = models.FileField(upload_to='factures/pdfs/', null=True, blank=True)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-created_at']
        unique_together = [['vendeur', 'reference']]

    def __str__(self):
        return f"{self.reference} ({self.client_nom})"

    @property
    def montant_total_apres_remise(self):
        return self.total_general - (self.remise or Decimal('0'))


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    quantite = models.DecimalField(max_digits=50, decimal_places=2)
    designation = models.CharField(max_length=500)
    prix_unitaire = models.DecimalField(max_digits=50, decimal_places=2)
    prix_total = models.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        verbose_name = "Ligne de facture"
        verbose_name_plural = "Lignes de facture"
        ordering = ['id']

    def __str__(self):
        return f"{self.designation} x{self.quantite}"


class Image(models.Model):
    slug = models.SlugField(default=uuid.uuid1)
    image = models.ImageField(upload_to='uploads/article', null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return str(self.slug)


class Promotion(models.Model):
    slug = models.SlugField(default=uuid.uuid1, editable=False)
    titre = models.CharField(max_length=20, null=True, blank=True)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)
    taux = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.titre or str(self.pk)


class Categorie(models.Model):
    slug = models.SlugField(default=uuid.uuid1)
    nom = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # promotion = models.ForeignKey(
    #     Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # images = models.FileField(upload_to='uploads/categori', null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['-created_at']

    def __str__(self):
        return self.nom


class Produit(models.Model):
    slug = models.SlugField(default=uuid.uuid1)
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(decimal_places=2, max_digits=50)
    promotion = models.ForeignKey(
        Promotion, related_name="promotion", on_delete=models.SET_NULL, null=True, blank=True)
    categorie = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, related_name='produit')
    type = models.CharField(max_length=100, choices=TYPE_ARTICLES)
    variations = models.ManyToManyField(
        'Variation', blank=True, default=[], related_name="produits")
    images = models.ManyToManyField(Image, blank=True, default=[])
    seuil = models.IntegerField(default=0, blank=True, null=True)
    stock = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    is_archived = models.BooleanField(default=False)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cout_de_revient = models.DecimalField(decimal_places=2, max_digits=50, default=0)
    prix_avec_promo = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if self.promotion and self.promotion.date_fin and self.promotion.date_fin >= timezone.now().date():
            self.prix_avec_promo = self.prix * (1 - (Decimal(self.promotion.taux) / 100))
        super(Produit, self).save(*args, **kwargs)

    def verify_stock(self, quantite, variations=None):
        if self.stock < quantite:
            return False
        if variations:
            try:
                first_variation = variations[0]
                variation_id = first_variation.id if isinstance(first_variation, Variation) else first_variation
                variation = Variation.objects.get(id=variation_id)
                if variation and variation.quantite < quantite:
                    return False
            except (Variation.DoesNotExist, IndexError):
                return False
        return True

    def subtract_in_stock(self, quantite, variations):
        self.stock -= Decimal(quantite)
        if variations:
            try:
                first_variation = variations[0]
                variation_id = first_variation.id if isinstance(first_variation, Variation) else first_variation
                variation = Variation.objects.get(id=variation_id)
                if variation:
                    variation.quantite -= Decimal(quantite)
                    variation.save()
            except (Variation.DoesNotExist, IndexError):
                pass
        self.save()


class Variation(models.Model):
    slug = models.SlugField(default=uuid.uuid1)
    taille = models.CharField(max_length=20, null=True, blank=True)
    couleur = models.CharField(max_length=50, null=True)
    quantite = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    seuil = models.IntegerField(default=0)
    images = models.ManyToManyField(Image, default=[], blank=True)
    active = models.BooleanField(default=False)
    produit = models.ForeignKey(
        Produit, on_delete=models.CASCADE, related_name='variation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.taille or ''} {self.couleur or ''}".strip() or str(self.pk)
