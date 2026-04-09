from django.shortcuts import render, redirect
from api.models import *
from django.contrib import messages
from ..forms import ProduitForm
# Create your views here.

def articleList(request):
    articles = Produit.objects.all()
    context = {'articles': articles}
    return render(request, 'dashboard/articles/listArticle.html', context)


def addArticle(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST['nom']
        description = request.POST['description']
        stock = request.POST['stock']
        prix = request.POST['prix']
        categorie__id = request.POST['categorie']

        # Récupérer l'instance de Category correspondante
        categorie = Produit.objects.get(id=categorie__id)

        # Créer un nouvel objet Article avec les données du formulaire
        new_article = Produit(
            nom=nom,
            description=description,
            stock=stock,
            prix=prix,
            categorie=categorie  # Utiliser l'instance de Category
        )
        new_article.save()

        messages.info(request, 'Article ajouté avec succès')  # Message d'information

        # Rediriger vers une page de confirmation ou une autre vue
        return redirect('articles')

    else:
        categories = Categorie.objects.all()
        context = {'categories': categories}
        return render(request, 'dashboard/articles/ajoutArticle.html', context)


def updateArticle(request, pk):
    produit = Produit.objects.get(pk=pk)
    if request.method == 'POST':
        Produit_form = ProduitForm(request.POST, instance=produit)
        if Produit_form.is_valid():
            # Récupérer l'ID de l'article depuis la requête POST
            produit_id = request.POST['produit_id']
            # Vérifier que l'ID correspond à l'ID de l'article dans la base de données
            if int(produit_id) == produit.id:
                Produit_form.save()
                messages.info(request, 'Produit modifié avec succès')
                return redirect('articles')
            else:
                messages.error(request, 'Une erreur s\'est produite lors de la mise à jour de l\'article.')
    else:
        # Créer le formulaire avec l'instance de l'article
        Produit_form = ProduitForm(instance=produit)

    # Ajouter l'ID de l'article au contexte
    context = {'Produit_form': Produit_form, 'produit_id': produit.id}
    return render(request, 'dashboard/articles/updateArticle.html', context)




def deleteArticle(request, pk):
        produit = Produit.objects.get(id=pk)
        if request.method == "POST":
            produit.delete()
            messages.info(request, 'Produit supprimée avec success')

            return redirect('articles')
        context = {"article":produit}
        return render(request, 'dashboard/articles/deleteArticle.html', context)

