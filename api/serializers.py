from rest_framework import serializers
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

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

# (VendeurAddSerializer / VendeurGetSerializer définis en tête de fichier)