from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # authentification
    # path('create-superadmin/', views.CreateSuperAdminView.as_view(), name='create-superadmin'),
    path('login/', views.LoginView.as_view()),
    path('verify-otp/', views.VerifyOTPView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('forgot-password/', views.ForgotPasswordView.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
    
    # Création de comptes vendeurs
    path('vendeurs/', views.VendeurRegisterAPIListView.as_view(), name='vendeur-register'),

    # Vendeurs
    # path('vendeurs/', views.VendeurAPIListView.as_view(), name='api-vendors-list'),
    # path('vendeurs/<slug:slug>/', views.VendeurAPIView.as_view(), name='api-vendors-detail'),
    # Produits par vendeur
    # path('vendeurs/<int:vendeur_id>/produits/', views.ProduitByVendeurAPIListView.as_view(), name='api-vendeur-produits'),
    # Catégories globales (list + create, détail par slug)
    # path('vendeur/categories/create/', views.CategorieAPIListView.as_view(), name='api-categories-list'),
    # path('vendeurs/<int:vendeur_id>/categories/', views.CategorieByVendeurAPIListView.as_view(), name='api-vendeur-categories'),
    # path('categorie/<slug:slug>/', views.CategorieAPIView.as_view(), name='api-categorie-detail'),
    # Produits (création + détail par slug)
#     path('vendeur/produits/create/', views.ProduitAPIListView.as_view(), name='api-produits-list'),
#     path('produits/<slug:slug>/', views.ProduitAPIView.as_view(), name='api-produit-detail'),
#     # Variations
#     path('variations/', views.VariationAPIListView.as_view(), name='api-variations-list'),
#     path('variations/<slug:slug>/', views.VariationAPIView.as_view(), name='api-variation-detail'),
#     # Factures (vendeur connecté)
#     path('vendeur/factures/', views.FactureListCreateAPIView.as_view(), name='api-factures-list-create'),
#     path('factures/<slug:slug>/', views.FactureDetailAPIView.as_view(), name='api-facture-detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
