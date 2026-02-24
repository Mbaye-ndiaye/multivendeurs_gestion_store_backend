from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone
from easy_password_generator import PassGen

from api.models import *
from api.serializers import *
from api.email_utils import send_vendeur_credentials


class VendeurAPIListView(generics.ListCreateAPIView):
    """
    Endpoint API pour lister et créer des vendeurs.
    GET /api/vendors/ : Liste tous les vendeurs
    POST /api/vendors/ : Crée un nouveau vendeur (réservé aux admins/superadmins)
    """
    queryset = Vendeur.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VendeurAddSerializer
        return VendeurGetSerializer
    
    def get(self, request, *args, **kwargs):
        """
        Liste tous les vendeurs (accessible à tous les utilisateurs authentifiés).
        """
        vendeurs = Vendeur.objects.all().order_by('-created_at')
        serializer = VendeurGetSerializer(vendeurs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Crée un nouveau vendeur.
        Réservé aux utilisateurs avec user_type == ADMIN ou SUPERADMIN.
        Génère automatiquement un mot de passe et l'envoie par email.
        """
        # Vérification des permissions
        if not (request.user.user_type == ADMIN or request.user.user_type == SUPERADMIN):
            return Response(
                {"message": "Vous n'êtes pas autorisé à ajouter un vendeur"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Génération automatique du mot de passe
        pwo = PassGen(minlen=8, minuc=1, minlc=1, minnum=1, minsc=1)
        password = pwo.generate()
        
        # Validation des données
        serializer = VendeurAddSerializer(data=request.data)
        if serializer.is_valid():
            # Création du vendeur
            vendeur = serializer.save()
            
            # Définir le mot de passe et le type d'utilisateur
            vendeur.password = make_password(password)
            vendeur.user_type = VENDEUR
            vendeur.save()
            
            # Envoi des identifiants par email
            send_vendeur_credentials(vendeur, password)
            
            # Retourner les données du vendeur créé (sans le mot de passe)
            response_serializer = VendeurGetSerializer(vendeur)
            return Response(
                {
                    **response_serializer.data,
                    "message": "Vendeur créé avec succès. Les identifiants ont été envoyés par email."
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendeurAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint API pour récupérer, modifier ou supprimer un vendeur spécifique.
    GET /api/vendors/<id>/ : Détails d'un vendeur
    PUT /api/vendors/<id>/ : Modifier un vendeur
    DELETE /api/vendors/<id>/ : Supprimer un vendeur (réservé aux admins/superadmins)
    """
    queryset = Vendeur.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VendeurAddSerializer
        return VendeurGetSerializer
    
    def delete(self, request, *args, **kwargs):
        """
        Supprime un vendeur (réservé aux admins/superadmins).
        """
        if not (request.user.user_type == ADMIN or request.user.user_type == SUPERADMIN):
            return Response(
                {"message": "Vous n'êtes pas autorisé à supprimer un vendeur"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().delete(request, *args, **kwargs)
