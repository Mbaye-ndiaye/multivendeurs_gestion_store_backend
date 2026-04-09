from api.models import *
from django import forms
from django.forms import ModelForm, TextInput, NumberInput,FileInput, Select



class CategorieForm(ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'images', 'vendeur']
        widgets = {
            'nom': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nom'
                }),
            'description': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Quantité'
                }),
            'images': FileInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;'
                }),
            'vendeur': Select(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;'
                }),
        }
