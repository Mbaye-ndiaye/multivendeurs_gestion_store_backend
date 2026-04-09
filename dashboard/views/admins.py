from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from api.models import *
import requests
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from api.notifications import Notif as notify
from backend.settings import API_URL
from api.utils import REGEX, Utils
from easy_password_generator import PassGen
from django.contrib import messages
from api.notifications import APP_NAME
from ..forms import AdminForm
# from ..forms import VendeurUpdateForm
from api.serializers import *


def adminList(request):
    admins = AdminUser.objects.all()
    context = {'admins': admins}
    return render(request, 'dashboard/admins/listAdmin.html', context)

def adminCreate(request):

    message=""
    if request.method == 'POST':
        pwo =PassGen(minlen=8, minuc=1, minlc=1, minnum=1, minsc=1)
        password_ = pwo.generate()
        telephone = request.POST['telephone']
        if telephone and '+221' not in telephone:
            telephone="+221"+telephone

        nom=request.POST['name']
        prenom=request.POST['firstname']
        adresse=request.POST['adresse']
        email=request.POST['email']
        pays=request.POST['pays']
        user_type=ADMIN
        admin_type=ADMIN
        
        try:
            admin=AdminUser.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                adresse=adresse,
                email=email,
                pays=pays,
                password=make_password(password_),
                user_type=user_type,
                admin_type=admin_type
            )

           


            subject, to = f"Bienvenu 🎉 sur GESTION STOCK",email
            template_src = 'mail_notification.html'
            contenu = f"Félicitations! Votre compte vient d'être créé  sur GESTION STOCK."
            context = {
                'settings': settings,
                "user":admin,
                "contenu":contenu,
                "id":"true",
                "APP_NAMES":"GESTION STOCK",
                "password":password_,
                "sujet":subject,
                "year":timezone.now().year
                }
            notify.send_email("GESTION STOCK",subject, to, template_src, context)
            messages.info(request, 'Vendeur ajouté avec succès')
        except ValidationError as e:
             # Gérer les erreurs de validation (par exemple, e.message contiendra des détails sur l'erreur).
            message="erreur des champs"
            messages.error(request, f"Erreur de validation: {e.message}")
            return render(request, 'dashboard/admins/ajoutAdmin.html',{"message":message})
        except IntegrityError as e:
            message="email et/ou numéro de téléphone dupliqué "
            # Gérer les erreurs d'intégrité (duplications d'email ou de numéro de téléphone).
            messages.error(request, f"Erreur d'intégrité: {e}")
            return render(request, 'dashboard/admins/ajoutAdmin.html',{"message":message})


        return redirect('admins')
        # context = {'Vendeur':Vendeur}


    return render(request, 'dashboard/admins/ajoutAdmin.html',{"message":message})