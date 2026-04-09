from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models import *
# Create your views here.



@login_required(login_url='dashboard-login')
def home(request):

    produits = Produit.objects.all().count()
    vendeurs = Vendeur.objects.all().count()
    acheteurs = User.objects.filter(user_type="ACHETEUR").count()

    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    if date_debut and date_fin:
        start_date = timezone.datetime.strptime(date_debut, '%d-%m-%Y')
        end_date = timezone.datetime.strptime(date_fin, '%d-%m-%Y')
        total_produits = Produit.objects.filter(created_at__gte=start_date, created_at__lte=end_date).count()

    context = {
        "produits": produits,
        "vendeurs": vendeurs,
        "acheteurs": acheteurs,
        "date_debut": date_debut,
        "date_fin": date_fin,
    }

    return render(request, 'dashboard/dashboard.html', context)