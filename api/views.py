from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Sum
from decimal import Decimal
from easy_password_generator import PassGen

from api.models import *
from api.serializers import *
from api.email_utils import send_vendeur_credentials
from api.pagination import KgPagination
from api.images import get_images
from rest_framework_tracking.mixins import LoggingMixin, BaseLoggingMixin
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
class LoginView(LoggingMixin, generics.CreateAPIView):
    permission_classes = (

    )
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        if 'email' in request.data and request.data['email']:
            if 'password' in request.data and request.data['password']:
                try:
                    email = request.data['email']
                    if "221" in email and "+221" not in email:
                        email = "+"+email
                    search_items = User.objects.filter(
                        telephone__icontains=email)
                    if search_items.exists():
                        item1 = User.objects.get(telephone=email)
                        if item1:
                            token = jwt_encode_handler(
                                jwt_payload_handler(item1))
                            return Response({'token': token, 'data': UserGetSerializer(item1).data}, status=200)

                    else:
                        email = request.data['email']
                        search_item = User.objects.filter(email__iexact=email)
                        if search_item.exists():
                            item = search_item.last()
                            if item and item.email != email:
                                email = item.email
                                request.data['email'] = email
                        item = User.objects.get(email=email)
                        user = authenticate(
                            request, email=email, password=request.data['password'])

                        # if item.is_archived:
                        #     return Response({"message": f"Votre compte a été archivé. Pour plus d'informations, veuillez contacter l'équipe de {APP_NAME}."}, status=400)

                        if item and not item.is_active:
                            return Response({
                                "status": "failure",
                                "message": "Ton compte n'a pas encore activé par l'admin."},
                                status=401)

                        elif user:
                            token = jwt_encode_handler(
                                jwt_payload_handler(user))
                            return Response({'token': token, 'data': UserGetSerializer(user).data}, status=200)

                        else:
                            return Response({"message": "Vos identifiants sont incorrects"}, status=400)
                except User.DoesNotExist:
                    return Response({"status": "failure", "message": "Ce compte n'existe pas. Veuillez-vous enregistrer"}, status=400)
            return Response({"message": "Votre mot de passe est requis"}, status=401)

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
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    
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




class CategorieAPIListView(generics.ListCreateAPIView):
    """GET /api/categories/ | POST /api/categories/"""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        nom = request.data.get('nom')
        if nom and Categorie.objects.filter(nom__iexact=nom, is_archived=False).exists():
            return Response(
                {"message": "Cette catégorie existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        items = Categorie.objects.filter(is_archived=False).order_by('-pk')
        limit = request.query_params.get('limit')
        return KgPagination.get_response(limit, items, request, CategorieGetSerializer)


class CategorieAPIView(generics.RetrieveAPIView):
    """GET /api/categorie/<slug>/ | PUT | DELETE"""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get(self, request, slug, format=None):
        try:
            item = Categorie.objects.get(slug=slug)
            serializer = CategorieGetSerializer(item)
            return Response(serializer.data)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug, format=None):
        try:
            item = Categorie.objects.get(slug=slug)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorieSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        try:
            item = Categorie.objects.get(slug=slug)
        except Categorie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if Produit.objects.filter(categorie=item, is_archived=False).exists():
            return Response(
                {"message": "Vous ne pouvez pas supprimer cette catégorie, des produits y sont liés."},
                status=status.HTTP_400_BAD_REQUEST
            )
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategorieByVendeurAPIListView(generics.ListAPIView):
    """GET /api/vendeurs/<id>/categories/ — catégories d'un vendeur."""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, vendeur_id, format=None):
        items = Categorie.objects.filter(vendeur_id=vendeur_id, is_archived=False).order_by('-pk')
        limit = request.query_params.get('limit')
        return KgPagination.get_response(limit, items, request, CategorieGetSerializer)




class ProduitAPIListView(generics.ListCreateAPIView):
    """POST /api/produits/ — création produit (avec images optionnelles)."""
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        nom = request.data.get('nom')
        if nom and Produit.objects.filter(nom__iexact=nom, is_archived=False).exists():
            return Response(
                {"message": "Ce nom de produit existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )
        image_ids = []
        if request.FILES.getlist('images'):
            image_ids = get_images(request.FILES.getlist('images'))
        data = request.data.copy()
        if 'images' in data:
            del data['images']
        serializer = ProduitSerializer(data=data)
        if serializer.is_valid():
            item = serializer.save()
            for iid in image_ids:
                item.images.add(iid)
            item.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProduitAPIView(generics.RetrieveAPIView):
    """GET /api/produits/<slug>/ | PUT | DELETE"""
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get(self, request, slug, format=None):
        try:
            item = Produit.objects.get(slug=slug)
            serializer = ProduitGetSerializer(item)
            return Response(serializer.data)
        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug, format=None):
        try:
            item = Produit.objects.get(slug=slug)
        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image_ids = []
        if request.FILES.getlist('images'):
            image_ids = get_images(request.FILES.getlist('images'))
        data = request.data.copy()
        if 'images' in data:
            del data['images']
        serializer = ProduitSerializer(item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            for iid in image_ids:
                item.images.add(iid)
            item.save()
            return Response(ProduitGetSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        try:
            item = Produit.objects.get(slug=slug)
        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProduitByVendeurAPIListView(generics.ListAPIView):
    """GET /api/vendeurs/<id>/produits/ — produits d'un vendeur (filtres: q, categorie, sous_categorie, prix_min, prix_max, stock)."""
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, vendeur_id, format=None):
        items = Produit.objects.filter(vendeur_id=vendeur_id, is_archived=False).order_by('-pk')
        q = request.query_params.get('q')
        categorie = request.query_params.get('categorie')
        prix_min = request.query_params.get('prix_min')
        prix_max = request.query_params.get('prix_max')
        stock = request.query_params.get('stock')
        if stock == "0":
            items = items.filter(stock=0)
        elif stock == "1":
            items = items.filter(stock__gt=0)
        if prix_min and prix_max:
            items = items.filter(prix__gte=prix_min, prix__lte=prix_max)
        if q:
            items = items.filter(Q(nom__icontains=q) | Q(description__icontains=q))
        if categorie:
            items = items.filter(categorie__slug=categorie)
        # if sous_categorie:
        #     slugs = [s.strip() for s in sous_categorie.split(',') if s.strip()]
            # if slugs:
            #     items = items.filter(sous_categorie__slug__in=slugs)
        limit = request.query_params.get('limit')
        return KgPagination.get_response(limit, items, request, ProduitGetSerializer)




class VariationAPIListView(generics.ListCreateAPIView):
    """GET /api/variations/ | POST /api/variations/"""
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        items = Variation.objects.all().order_by('-pk')
        limit = request.query_params.get('limit')
        return KgPagination.get_response(limit, items, request, VariationGetSerializer)

    def post(self, request, format=None):
        data = request.data.copy()
        image_ids = []
        if request.FILES.getlist('images'):
            image_ids = get_images(request.FILES.getlist('images'))
        if 'images' in data:
            del data['images']
        serializer = VariationSerializer(data=data)
        if serializer.is_valid():
            item = serializer.save()
            for iid in image_ids:
                item.images.add(iid)
            item.save()
            item.produit.variations.add(item)
            item.produit.stock += Decimal(str(item.quantite))
            item.produit.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VariationAPIView(generics.RetrieveAPIView):
    """GET /api/variations/<slug>/ | PUT | DELETE"""
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get(self, request, slug, format=None):
        try:
            item = Variation.objects.get(slug=slug)
            serializer = VariationGetSerializer(item)
            return Response(serializer.data)
        except Variation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug, format=None):
        try:
            item = Variation.objects.get(slug=slug)
        except Variation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        image_ids = []
        if request.FILES.getlist('images'):
            image_ids = get_images(request.FILES.getlist('images'))
        if 'images' in data:
            del data['images']
        serializer = VariationSerializer(item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            for iid in image_ids:
                item.images.add(iid)
            item.save()
            total_quantite = Variation.objects.filter(produit=item.produit).aggregate(sum_quantite=Sum('quantite'))
            sum_of_quantite = total_quantite.get('sum_quantite') or Decimal('0')
            item.produit.stock = sum_of_quantite
            item.produit.save()
            return Response(VariationGetSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        try:
            item = Variation.objects.get(slug=slug)
        except Variation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
