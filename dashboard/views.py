from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
from easy_password_generator import PassGen

from api.models import *
from .forms import VendorForm


def _is_superadmin(user):
    """
    Vérifie que l'utilisateur est super admin.
    Comme dans Easymarket : vérifie is_superuser OU user_type == SUPERADMIN ou ADMIN.
    """
    if not user.is_authenticated:
        return False
    # Vérifie si superuser Django OU type admin/superadmin
    from api.models import ADMIN, SUPERADMIN
    return (user.is_superuser or 
            user.user_type == ADMIN or 
            user.user_type == SUPERADMIN)


def login_view(request):
    """
    Page de connexion pour accéder au dashboard SuperAdmin.
    """
    if request.user.is_authenticated:
        return redirect("dashboard-home")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard-home")

    return render(request, "dashboard/login.html", {"form": form})


@login_required
def logout_view(request):
    """
    Déconnexion de l'utilisateur actuel.
    """
    logout(request)
    return redirect("dashboard-login")


@login_required
@user_passes_test(_is_superadmin)
def home(request):
    """
    Page d'accueil du dashboard SuperAdmin.
    Affiche les statistiques des vendeurs.
    """
    # Statistiques des vendeurs
    stats_vendeurs = {
        'total': Vendeur.objects.count(),
        'actifs': Vendeur.objects.filter(is_active=True).count(),
        'bloques': Vendeur.objects.filter(is_active=False).count(),
    }
    
    context = {
        'stats_vendeurs': stats_vendeurs
    }
    return render(request, "dashboard/home.html", context)


@login_required
@user_passes_test(_is_superadmin)
def vendeur_list(request):
    """
    Liste des vendeurs gérés par le superAdmin.
    Avec statistiques : total, actifs, bloqués, inactifs.
    """
    vendeurs = Vendeur.objects.all().order_by("-created_at")
    
    # Calcul des statistiques
    stats = {
        'total': Vendeur.objects.count(),
        'actifs': Vendeur.objects.filter(is_active=True).count(),
        'bloques': Vendeur.objects.filter(is_active=False).count(),
        'inactifs': Vendeur.objects.filter(is_active=False).count(),
    }
    
    context = {
        "vendeurs": vendeurs,
        "stats": stats
    }
    return render(request, "dashboard/vendeurs/list.html", context)


@login_required
@user_passes_test(_is_superadmin)
def vendeur_create(request):
    """
    Création d'un vendeur par le superAdmin.    """
    message = ""
    
    if request.method == "POST":
        # Récupération des données du formulaire
        nom = request.POST.get('nom', '')
        prenom = request.POST.get('prenom', '')
        telephone = request.POST.get('telephone', '')
        email = request.POST.get('email', '')
        adresse = request.POST.get('adresse', '')
        pays = request.POST.get('pays', '')
        nom_de_la_boutique = request.POST.get('nom_de_la_boutique', '')
        couleur = request.POST.get('couleur', '')
        domaine = request.POST.get('domaine', '')
        
        # Génération automatique du mot de passe (comme Easymarket)
        pwo = PassGen(minlen=8, minuc=1, minlc=1, minnum=1, minsc=1)
        password_ = pwo.generate()
        
        # Formatage du téléphone (ajouter +221 si nécessaire)
        if telephone and '+221' not in telephone:
            telephone = "+221" + telephone
        
        try:
            # Création du vendeur (hérite de User)
            vendeur = Vendeur.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                adresse=adresse,
                pays=pays,
                email=email,
                password=make_password(password_),
                user_type=VENDEUR,
                nom_de_la_boutique=nom_de_la_boutique,
                # couleur=couleur if couleur else None,
                domaine=domaine if domaine else None,
            )
            
            # Pour l'instant, on affiche juste un message de succès
            messages.success(request, f'Vendeur ajouté avec succès. Mot de passe généré: {password_}')
            return redirect("dashboard-vendeurs")
            
        except ValidationError as e:
            message = "Erreur de validation des champs"
            messages.error(request, f"Erreur de validation: {e}")
        except IntegrityError as e:
            message = "Email et/ou numéro de téléphone déjà utilisé"
            messages.error(request, f"Erreur d'intégrité: {e}")
        except Exception as e:
            message = f"Erreur lors de la création: {str(e)}"
            messages.error(request, message)
    
    # GET : afficher le formulaire
    context = {"form": VendorForm(), "message": message}
    return render(request, "dashboard/vendeurs/create.html", context)

