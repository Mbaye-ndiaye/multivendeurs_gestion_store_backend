from api.models import *
from api.notifications import Notif as notify
from api.serializers import OrderSerializer
from backend import settings
from django.utils import timezone
from api.operations import check_service_order, send_sms
from background_task import background
from backend.settings import APP_NAME






@background(schedule=0)
def notification_after_add_vendeur(item_id, password):
    item = Vendeur.objects.get(id=item_id)
    APP_NAMES = item.nom_de_la_boutique
    user_type = item.user_type.upper()
    contenu = f"Nous vous informons qu'un compte {user_type} vient juste d'être crée pour vous sur la plateforme {APP_NAME}."
    subject = f"Création d'un compte {user_type}"
    to = item.email
    template_src = 'mail_notification.html'
    context = {
        "user": item,
        "settings": settings,
        "nom": item.nom,
        "prenom": item.prenom,
        "contenu": contenu,
        "email": item.email,
        "password": password,
        "id": "true",
        "sujet": subject,
        "year": timezone.now().year,
        "APP_NAMES": APP_NAMES
    }
    notify.send_email(APP_NAMES, subject, to,
                      template_src, context_dict=context)


# @background(schedule=0)
# def notification_after_facturation(item_id):
#     item = Facturation.objects.get(id=item_id)
#     APP_NAMES = item.order.vendeur.nom_de_la_boutique
#     contenu = f"Nous vous informons que la facture de votre commande {item.order.code_commande} est désormais disponible. Veuillez trouver ci-joint la facture de ladite commande."
#     subject = f"Facturation de votre commande {item.order.code_commande}"
#     to = item.order.user.email if item.order.user else item.order.email_client
#     template_src = 'mail_notification.html'
#     context = {
#         "user": item,
#         "settings": settings,
#         "nom": item.order.user.nom if item.order.user else "",
#         "prenom": item.order.user.prenom if item.order.user else "",
#         "contenu": contenu,
#         "sujet": subject,
#         "year": timezone.now().year,
#         "APP_NAMES": APP_NAMES
#     }
#     notify.send_email(APP_NAMES, subject, to, template_src,
#                       context_dict=context, file=item.facture)
