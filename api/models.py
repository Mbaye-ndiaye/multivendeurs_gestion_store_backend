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

COMMANDE = 'commande'
SEUIL = 'seuil'
BLOCAGE = 'blocage'
DEBLOCAGE = 'deblocage'
DEPENSE = 'depense'

NOTIF_TYPE = (
    (COMMANDE, COMMANDE),
    (SEUIL, SEUIL),
    (BLOCAGE, BLOCAGE),
    (DEBLOCAGE, DEBLOCAGE),
    (DEPENSE, DEPENSE),
)
CASH = 'CASH'
WAVE = 'WAVE'
ORANGE_MONEY = 'ORANGE_MONEY'
STRIPE = 'STRIPE'
PAYONEER = 'PAYONEER'
CHEQUE = "chèque"
PAYPAL = "paypal"
MOOV = "moov"
MONEY_FLOOZ = "money_flooz"
TMONEY = "tmoney"
PAYGATE = "paygate"
PAYTECH = "paytech"
PAYMENT_MODE = (
    ('ORANGE_SN_API_CASH_OUT', 'ORANGE_MONEY'),
    ('WAVE_SN_API_CASH_OUT', 'WAVE'),
    ('BANK_TRANSFER_SN_API_CASH_OUT', 'VIREMENT_BANCAIRE'),
    (WAVE, WAVE),
    (STRIPE, STRIPE),
    (CASH, CASH),
    (PAYONEER, PAYONEER),
    (PAYPAL, PAYPAL),
    (CHEQUE, CHEQUE),
    (MOOV, MOOV),
    (MONEY_FLOOZ, MONEY_FLOOZ),
    (TMONEY, TMONEY),
    (PAYGATE, PAYGATE),
    (PAYTECH, PAYTECH),
    (ORANGE_MONEY, ORANGE_MONEY),
)


NOUVELLE_COMMANDE = 'NOUVELLE_COMMANDE'
EN_COURS_DE_TRAITEMENT = 'EN_COURS_DE_TRAITEMENT'
EN_COURS_DE_LIVRAISON = 'EN_COURS_DE_LIVRAISON'
LIVRE = 'LIVRE'
ANNULE = 'ANNULE'
ORDER_STATUS = (
    ('NOUVELLE_COMMANDE', NOUVELLE_COMMANDE),
    ('EN_COURS_DE_TRAITEMENT', EN_COURS_DE_TRAITEMENT),
    ('EN_COURS_DE_LIVRAISON', EN_COURS_DE_LIVRAISON),
    ('LIVRE', LIVRE),
    ('ANNULE', ANNULE),

)
PAYEE = "payée"
NON_PAYEE = "non payée"
PARTIELLEMENT_PAYEE = "partiellement payée"
PAID_STATUS = (
    (PAYEE, PAYEE),
    (NON_PAYEE, NON_PAYEE),
    (PARTIELLEMENT_PAYEE, PARTIELLEMENT_PAYEE),
)
EUR = 'EUR'
USD = 'USD'
XOF = 'XOF'
CURRENCY = (
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('XOF', 'XOF')
)

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
    # api_key = models.CharField(max_length=200, blank=True, null=True)
    devise = models.CharField(max_length=20, choices=CURRENCY, default=XOF)

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
        
        # Générer une clé API si elle n'existe pas
        # if not self.api_key:
        #     api_key = secrets.token_hex(32)  # 32 bytes = 64 characters
        #     hashed_api_key = hashlib.sha256(api_key.encode()).hexdigest()
        #     self.api_key = hashed_api_key
        
        super().save(*args, **kwargs)
