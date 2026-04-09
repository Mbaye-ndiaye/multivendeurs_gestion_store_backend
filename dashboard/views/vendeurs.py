from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from api.models import *
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from api.notifications import Notif as notify
from backend import settings
from backend.settings import API_URL
from api.utils import REGEX, Utils
from django.utils import timezone
from easy_password_generator import PassGen
from django.contrib import messages
from api.notifications import APP_NAME
from ..forms import VendeurForm
from ..forms import VendeurUpdateForm
from api.serializers import *
from api.utils import REGEX, Utils as my_utils


def vendeurListFiltre(request):
    vendeurs = Vendeur.objects.all().order_by('-created_at')
    # Filtrer les commandes si un vendeur est sélectionné
    vendeur_id = request.GET.get('vendeur')
    # if vendeur_id:
    #     commandes = Order.objects.filter(vendeur_id=vendeur_id)
    # else:
    #     commandes = Order.objects.all()

    context = {
        # 'orders': commandes,
        'vendeurs': vendeurs
    }
    return render(request, 'dashboard/commandes/listCommandes.html', context)


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


 
            
def vendeur_create(request):
    # Vendeur_form = VendeurForm()
    message=""    
    services = Service.objects.all()
         
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        
        telephone = request.POST['telephone']
        email = request.POST['email']
        pwo = PassGen(minlen=8, minuc=1, minlc=1, minnum=1, minsc=1)
        password_ = pwo.generate()
        user_type = 'VENDEUR'
        nom_de_la_boutique = request.POST['nom_de_la_boutique']
        couleur = request.POST['couleur']
        domaine = request.POST['domaine']
       
        adresse = request.POST['adresse']
        pays = request.POST['pays']
        # paygate_api_key = request.POST['paygate_api_key']
        # paygate_network = request.POST['paygate_network']
        # wave_is_set = request.POST['wave_is_set']
        # stripe_is_set = request.POST['stripe_is_set']
        # paygate_is_set = request.POST['paygate_is_set']   
        service = None
        if "service" in request.POST and request.POST['service']:
            service_id = request.POST['service']
            service = Service.objects.filter(id=service_id).first()
        if '+221' not in telephone:
            telephone="+221"+telephone
        

        try:
            vendeur=Vendeur.objects.create(
                
                nom=nom,
                prenom=prenom,
                adresse=adresse,
                pays=pays,
                telephone=telephone,
                email=email,
                password= make_password(password_),
                user_type=user_type,
                nom_de_la_boutique=nom_de_la_boutique,
                couleur=couleur,
                domaine=domaine,
                service=service,
            )
            
            

            
        
            subject, to = f"Bienvenue 🎉 sur GESTION STOCK",email
            template_src = 'mail_notification.html'
            contenu = f"Félicitations! Votre compte vient d'être créé  sur GESTION STOCK."
            context = {
                'settings': settings,
                "user":vendeur,
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
                return render(request, 'dashboard/vendeurs/ajoutVendeur.html',{"message":message,"services":services})
        except IntegrityError as e:
                message="email et/ou numéro de téléphone dupliqué "
                # Gérer les erreurs d'intégrité (duplications d'email ou de numéro de téléphone).
                messages.error(request, f"Erreur d'intégrité: {e}")
                return render(request, 'dashboard/vendeurs/ajoutVendeur.html',{"message":message,"services":services})

        return redirect('vendeurs')
            # context = {'Vendeur':Vendeur}
    return render(request, 'dashboard/vendeurs/ajoutVendeur.html',{"services":services})


def updateVendeur(request, pk):
    vendeur = Vendeur.objects.get(pk=pk)
    # 
    if request.method == 'POST':
       vendeur_form = VendeurUpdateForm(request.POST, instance=vendeur)
       if vendeur_form.is_valid():
            # Récupérer l'ID de l'article depuis la requête POST
            vendeur_id = request.POST['vendeur_id']
            # Vérifier que l'ID correspond à l'ID de l'article dans la base de données
            if int(vendeur_id) == vendeur.id:
                vendeur_form.save()
                messages.info(request, 'Catégorie modifiée avec succes')
                return redirect('vendeurs')
            else:
                messages.error(request, 'Une erreur s\'est produite lors de la mise à jour de la catégorie.')
    else:
        # Créer le formulaire avec l'instance de l'article
        vendeur_form = VendeurUpdateForm(instance=vendeur)
    context = {'vendeur_id':vendeur.id, 'vendeur_form':vendeur_form}
    return render(request, 'dashboard/vendeurs/updateVendeur.html',context)


def blocVendeur(request, pk):
    item = Vendeur.objects.get(id=pk)
        
    if request.method == "POST":
        item.is_active = False
        item.save()
        subject, to = f" Notification de blocage de votre compte sur {APP_NAME}",item.email
        template_src = 'mail_notification.html'
        contenu = f"Nous vous informons que votre compte sur {APP_NAME} a été bloqué en raison du non-paiement de vos factures récentes. Nous comprenons que des circonstances imprévues peuvent survenir, mais il est important de maintenir les paiements à jour pour continuer à profiter de nos services. Votre compte restera bloqué jusqu'à ce que le paiement soit reçu et vérifié. Pour réactiver votre compte, veuillez effectuer un paiement immédiat. Une fois le paiement effectué, votre compte sera réactivé dans les plus brefs délais. Si vous avez des questions ou avez besoin d'assistance pour résoudre ce problème, n'hésitez pas à nous contacter à l'adresse suivante : contact@easymarket.sn Notre équipe de support est là pour vous aider. Nous vous remercions de votre compréhension et de votre coopération pour régler cette situation."
        context = {
            'settings': settings,
            "user":item,
            "prenom":item.prenom,
            "nom":item.nom,
            "APP_NAMES":APP_NAME,
            "idts":"true",
            "contenu":contenu,
            "id":"false",
            "sujet":"",
            "year":timezone.now().year
        }
        notify.send_email("GESTION STOCK",subject, to, template_src, context)
        messages.info(request, 'Vendeur bloqué avec succès')
        return redirect('vendeurs')
    
    context = {"vendeur":item}
    return render(request, 'dashboard/vendeurs/blocVendeur.html', context)
def deblocVendeur(request, pk):
        item = Vendeur.objects.get(id=pk)
        if request.method == "POST":
            item.is_active = True
            item.save()
            subject, to = f" Notification de déblocage de votre compte sur {APP_NAME}",item.email
            template_src = 'mail_notification.html'
            contenu = f"Nous vous informons que votre compte sur {APP_NAME} a été débloqué. Nous vous remercions de votre compréhension et de votre coopération pour régler cette situation."
            context = {
            'settings': settings,
            "user":item,
            "prenom":item.prenom,
            "nom":item.nom,
            "contenu":contenu,
            "APP_NAMES":APP_NAME,
            "idts":"true",
            "id":"false",
            "sujet":"",
            "year":timezone.now().year
            }
            notify.send_email("GESTION STOCK",subject, to, template_src, context)
            messages.info(request, 'Vendeur débloqué avec succès')

            return redirect('vendeurs')
        context = {"vendeur":item}
        return render(request, 'dashboard/vendeurs/unblockVendeur.html', context)


def deleteVendeur(request, pk):
    
    item = Vendeur.objects.get(id=pk)
    if request.method == "POST":
        
        if request.user.is_superuser or request.user.user_type == ADMIN:
            randomstring = my_utils.random_string_generator(12,
            "userdeletion")
            email = item.email
            user_type = item.user_type
            item.email = randomstring+""+item.email
            item.telephone = randomstring+""+item.telephone
            item.deletion_id = email
            item.user_type = DELETED
            item.is_archive = True
            item.is_active=False
            item.deletion_type = user_type
            item.save()
            messages.info(request, 'Vendeur supprimé avec succés')
            return redirect('vendeurs')
    context = {"vendeur":item}
    return render(request, 'dashboard/vendeurs/deleteVendeur.html', context)
        

# def detailsVendeur(request, pk):
#     vendeur= Vendeur.objects.get(id=pk)
#     context = {"vendeur":vendeur}
#     return render(request, 'dashboard/vendeurs/details_vendeur.html', context)



def detailsVendeur(request, pk):
    vendeur= Vendeur.objects.get(id=pk)
    context = {"vendeur":vendeur}
    return render(request, 'dashboard/vendeurs/details_vendeur.html', context)
