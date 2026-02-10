from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from api.models import Vendor
from .forms import VendorForm


def _is_superadmin(user):
    """
    Vérifie que l'utilisateur est super admin.
    Pour l'instant on se base sur is_superuser du modèle User par défaut.
    """
    return user.is_authenticated and user.is_superuser


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
    """
    return render(request, "dashboard/home.html")


@login_required
@user_passes_test(_is_superadmin)
def vendor_list(request):
    """
    Liste des vendeurs gérés par le superAdmin.
    """
    vendors = Vendor.objects.all().order_by("-created_at")
    context = {"vendors": vendors}
    return render(request, "dashboard/vendors/list.html", context)


@login_required
@user_passes_test(_is_superadmin)
def vendor_create(request):
    """
    Création d'un vendeur par le superAdmin.
    """
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard-vendors")
    else:
        form = VendorForm()

    context = {"form": form}
    return render(request, "dashboard/vendors/create.html", context)

