from django.shortcuts import render, redirect
from api.models import *
from django.contrib import messages
from ..forms import CategorieForm
# Create your views here.

def categoryList(request):
    categories = Categorie.objects.all()
    context = {'categories': categories}
    return render(request, 'dashboard/categories/listCategory.html', context)


def addCategory(request):
    # Category_form = CategoryForm()
    if request.method == 'POST':
      nom = request.POST['nom']
      description = request.POST['description']
      images = request.POST['images']
      vendeur_id = request.POST['vendeur']

      vendeur = Vendeur.objects.get(pk=vendeur_id)
      categorie = Categorie.objects.create(
          nom=nom,
          description=description,
          images=images,
          vendeur=vendeur
        )
      categorie.save()
          
      messages.info(request, 'Catégorie ajoutée avec succès')
      return redirect('categories')
    # context = {'Category':Category}
    return render(request, 'dashboard/categories/ajoutCategory.html')


def updateCategory(request, pk):
    categorie = Categorie.objects.get(id=pk)
    
    if request.method == 'POST':
        categorie_form = CategorieForm(request.POST, instance=categorie)
        if categorie_form.is_valid():
            # Récupérer l'ID de l'article depuis la requête POST
            categorie_id = request.POST['categorie_id']
            # Vérifier que l'ID correspond à l'ID de l'article dans la base de données
            if int(categorie_id) == categorie.id:
                categorie_form.save()
                messages.info(request, 'Catégorie modifiée avec succes')
                return redirect('categories')
            else:
                messages.error(request, 'Une erreur s\'est produite lors de la mise à jour de la catégorie.')
    else:
        # Créer le formulaire avec l'instance de l'article
        categorie_form = CategorieForm(instance=categorie)
    context = {'categorie_form':categorie_form, 'categorie_id':categorie.id}
    return render(request, 'dashboard/categories/updateCategory.html', context)


def deleteCategory(request, pk):
        category = Categorie.objects.get(id=pk)
        if request.method == "POST":
            category.delete()
            messages.info(request, 'category supprimée avec succès')

            return redirect('categories')
        context = {"category":category}
        return render(request, 'dashboard/categories/deleteCategory.html', context)

