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
from api.email_utils import send_vendeur_credentials
from .forms import VendorForm


def _is_superadmin(user):
    """
    Vérifie que l'utilisateur est super admin.
    vérifie is_superuser OU user_type == SUPERADMIN ou ADMIN.
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
    : utilise email pour l'authentification.
    """
    if request.user.is_authenticated:
        return redirect("dashboard-home")

    if request.method == "POST":
        email = request.POST.get('username')  # AuthenticationForm utilise 'username' mais mappe vers USERNAME_FIELD
        password = request.POST.get('password')
        
        if email and password:
            # Authentifier avec email (USERNAME_FIELD = 'email')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                # Vérifier que c'est un admin/superadmin
                if user.is_superuser or user.user_type in ['admin', 'superadmin']:
                    # Vérifier si le compte est actif
                    if not user.is_active:
                        messages.error(request, 'Votre compte a été bloqué. Veuillez contacter le support.')
                    else:
                        login(request, user)
                        return redirect("dashboard-home")
                else:
                    messages.error(request, 'Accès réservé aux administrateurs.')
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    # Utiliser AuthenticationForm pour le rendu du formulaire
    form = AuthenticationForm(request, data=request.POST or None)
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
        
        # Génération automatique du mot de passe
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
            
            # Envoi des identifiants par email
            if send_vendeur_credentials(vendeur, password_):
                messages.success(request, 'Vendeur ajouté avec succès. Les identifiants ont été envoyés par email.')
            else:
                messages.warning(request, 'Vendeur ajouté, mais l\'envoi de l\'email a échoué. Communiquez les identifiants manuellement.')
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


@login_required
@user_passes_test(_is_superadmin)
def bloc_vendeur(request, pk):
    """
    Bloquer un vendeur
    Met is_active à False.
    """
    try:
        vendeur = Vendeur.objects.get(id=pk)
        
        if request.method == "POST":
            vendeur.is_active = False
            vendeur.save()
            
            # TODO: Envoyer un email de notification
            # notify.send_email(...)
            
            messages.success(request, f'Vendeur {vendeur.nom_de_la_boutique} bloqué avec succès')
            return redirect("dashboard-vendeurs")
        
        context = {"vendeur": vendeur}
        return render(request, "dashboard/vendeurs/bloc.html", context)
    
    except Vendeur.DoesNotExist:
        messages.error(request, "Vendeur introuvable")
        return redirect("dashboard-vendeurs")


@login_required
@user_passes_test(_is_superadmin)
def debloc_vendeur(request, pk):
    """
    Débloquer un vendeur.
    Met is_active à True.
    """
    try:
        vendeur = Vendeur.objects.get(id=pk)
        
        if request.method == "POST":
            vendeur.is_active = True
            vendeur.save()
            
            # TODO: Envoyer un email de notification
            # notify.send_email(...)
            
            messages.success(request, f'Vendeur {vendeur.nom_de_la_boutique} débloqué avec succès')
            return redirect("dashboard-vendeurs")
        
        context = {"vendeur": vendeur}
        return render(request, "dashboard/vendeurs/debloc.html", context)
    
    except Vendeur.DoesNotExist:
        messages.error(request, "Vendeur introuvable")
        return redirect("dashboard-vendeurs")

