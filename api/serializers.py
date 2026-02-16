from rest_framework import serializers
from api.models import *


class VendeurAddSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer un vendeur via l'API.
    Exclut les champs sensibles (password, permissions, etc.).
    """
    class Meta:
        model = Vendeur
        exclude = (
            'user_permissions', 
            'groups', 
            'is_superuser', 
            'is_staff', 
            'tokens', 
            'is_active', 
            'is_archive', 
            'password',
        )


class VendeurGetSerializer(serializers.ModelSerializer):
    """
    Serializer pour lire les données d'un vendeur via l'API.
    Exclut les informations sensibles.
    """
    class Meta:
        model = Vendeur
        exclude = (
            'user_permissions', 
            'groups', 
            'is_superuser',
            'is_staff', 
            'password', 
        )