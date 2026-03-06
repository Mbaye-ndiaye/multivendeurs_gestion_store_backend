from rest_framework import serializers
from api.models import *


# --- Vendeur (doit être avant CategorieGetSerializer / ProduitGetSerializer) ---

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, min_length=6, required=True)

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