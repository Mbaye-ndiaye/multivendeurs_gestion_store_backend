from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from decimal import Decimal
from datetime import timedelta

from django.utils import timezone

from api.models import *


# --- Vendeur (doit être avant CategorieGetSerializer / ProduitGetSerializer) ---
# class CreateSuperAdminSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(write_only=True, required=True, min_length=8)
#     nom = serializers.CharField(required=False, allow_blank=True)
#     prenom = serializers.CharField(required=False, allow_blank=True)

#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("Cet email est déjà utilisé.")
#         return value

#     def create(self, validated_data):
#         return User.objects.create_superuser(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             nom=validated_data.get('nom', ''),
#             prenom=validated_data.get('prenom', ''),
#             user_type='superadmin',
#             is_staff=True,
#             is_active=True
#         )
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, min_length=6, required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64, required=True)
    new_password = serializers.CharField(min_length=8, required=True)
    confirm_password = serializers.CharField(min_length=8, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

class UserGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            'user_permissions', 'groups', 'is_superuser',
            'is_staff', 'password')

class VendeurAddSerializer(serializers.ModelSerializer):
    """Serializer pour créer un vendeur via l'API."""
    class Meta:
        model = Vendeur
        exclude = (
            'user_permissions', 'groups', 'is_superuser', 'is_staff',
            'tokens', 'is_active', 'is_archive', 'password',
        )


class VendeurGetSerializer(serializers.ModelSerializer):
    """Serializer pour lire les données d'un vendeur via l'API."""
    class Meta:
        model = Vendeur
        exclude = (
            'user_permissions', 'groups', 'is_superuser', 'is_staff', 'password',
        )

class VendeurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendeur
        exclude = (
            'user_permissions', 'groups', 'is_superuser', 'is_staff', 'password')



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


# class SousCategorieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SousCategorie
#         fields = '__all__'


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'


class CategorieGetSerializer(serializers.ModelSerializer):
    vendeur = VendeurGetSerializer(read_only=True)
    # sous_categorie = serializers.SerializerMethodField('get_sous_categories')
    nbproduits = serializers.SerializerMethodField('get_nbproduits')
    promotion = PromotionSerializer(read_only=True)

    class Meta:
        model = Categorie
        fields = '__all__'

    # def get_sous_categories(self, obj):
    #     return SousCategorieSerializer(obj.sous_categorie.all(), many=True).data

    def get_nbproduits(self, obj):
        return Produit.objects.filter(categorie=obj, is_archived=False).count()


# class SousCategorieGetSerializer(serializers.ModelSerializer):
#     promotion = PromotionSerializer(read_only=True)

#     class Meta:
#         model = SousCategorie
#         fields = '__all__'


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'


class VariationProduitGetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Variation
        fields = '__all__'


class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'


class ProduitGetSerializer(serializers.ModelSerializer):
    vendeur = VendeurGetSerializer(read_only=True)
    variations = VariationProduitGetSerializer(many=True, read_only=True)
    categorie = CategorieGetSerializer(read_only=True)
    # sous_categorie = SousCategorieGetSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    promotion = PromotionSerializer(read_only=True)

    class Meta:
        model = Produit
        fields = '__all__'


class VariationGetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    produit = ProduitSerializer(read_only=True)

    class Meta:
        model = Variation
        fields = '__all__'

class ServiceSerializer(ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class ServiceGetSerializer(ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class LigneFactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneFacture
        fields = ('id', 'quantite', 'designation', 'prix_unitaire', 'prix_total')


class LigneFactureWriteSerializer(serializers.Serializer):
    quantite = serializers.DecimalField(max_digits=50, decimal_places=2)
    designation = serializers.CharField(max_length=500)
    prix_unitaire = serializers.DecimalField(max_digits=50, decimal_places=2)
    prix_total = serializers.DecimalField(max_digits=50, decimal_places=2)

    def validate(self, data):
        q = Decimal(str(data['quantite']))
        pu = Decimal(str(data['prix_unitaire']))
        pt = Decimal(str(data['prix_total']))
        attendu = (q * pu).quantize(Decimal('0.01'))
        if abs(pt - attendu) > Decimal('0.02'):
            raise serializers.ValidationError(
                "prix_total doit correspondre à quantite × prix_unitaire (tolérance 0,02)."
            )
        return data


class FactureCreateSerializer(serializers.Serializer):
    client_nom = serializers.CharField(max_length=500)
    client_telephone = serializers.CharField(max_length=50)
    reference = serializers.CharField(max_length=100)
    lignes = LigneFactureWriteSerializer(many=True)
    date_facture = serializers.DateField(required=False)
    date_echeance = serializers.DateField(required=False)
    remise = serializers.DecimalField(
        max_digits=50, decimal_places=2, required=False, default=0)
    paid_statut = serializers.ChoiceField(
        choices=FACTURE_PAID_STATUT, required=False, default=FACTURE_NON_PAYEE)

    def validate_lignes(self, value):
        if not value:
            raise serializers.ValidationError("Au moins une ligne est requise.")
        return value

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes')
        vendeur = self.context['vendeur']
        dtf = validated_data.pop('date_facture', None)
        dte = validated_data.pop('date_echeance', None)
        remise = validated_data.pop('remise', Decimal('0'))
        paid_statut = validated_data.pop('paid_statut', FACTURE_NON_PAYEE)
        if dtf is None:
            dtf = timezone.now().date()
        if dte is None:
            dte = dtf + timedelta(days=30)
        total = Decimal('0')
        for ligne in lignes_data:
            total += Decimal(str(ligne['prix_total']))
        facture = Facture.objects.create(
            vendeur=vendeur,
            client_nom=validated_data['client_nom'],
            client_telephone=validated_data['client_telephone'],
            reference=validated_data['reference'],
            total_general=total,
            date_facture=dtf,
            date_echeance=dte,
            remise=remise,
            paid_statut=paid_statut,
        )
        for ligne in lignes_data:
            LigneFacture.objects.create(facture=facture, **ligne)
        return facture


class VendeurRegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(read_only=True, default=VENDEUR)
    
    class Meta:
        model = Vendeur
        exclude = (
            'user_permissions', 'groups', 'is_superuser', 'is_staff')

    def create(self, validated_data, **extra_fields):
        vendeur = self.Meta.model(**validated_data)
        vendeur.set_password(validated_data['password'])
        vendeur.is_active = True
        vendeur.user_type = VENDEUR
        vendeur.save()
        return vendeur


class FactureDetailSerializer(serializers.ModelSerializer):
    lignes = LigneFactureSerializer(many=True, read_only=True)
    signature_vendeur = serializers.SerializerMethodField()
    facture_pdf_url = serializers.SerializerMethodField()
    nom_boutique = serializers.CharField(source='vendeur.nom_de_la_boutique', read_only=True)
    montant_total_apres_remise = serializers.ReadOnlyField()

    class Meta:
        model = Facture
        fields = (
            'slug', 'reference', 'client_nom', 'client_telephone',
            'nom_boutique', 'signature_vendeur', 'lignes', 'total_general',
            'date_facture', 'date_echeance', 'remise', 'paid_statut',
            'montant_total_apres_remise', 'facture_pdf_url', 'created_at',
        )

    def get_signature_vendeur(self, obj):
        v = obj.vendeur
        if not v.signature:
            return None
        request = self.context.get('request')
        url = v.signature.url
        if request:
            return request.build_absolute_uri(url)
        return url

    def get_facture_pdf_url(self, obj):
        if not obj.facture_pdf:
            return None
        request = self.context.get('request')
        u = obj.facture_pdf.url
        if request:
            return request.build_absolute_uri(u)
        return u

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

# (VendeurAddSerializer / VendeurGetSerializer définis en tête de fichier)