from api.models import *
from django import forms
from django.forms import ModelForm, TextInput, NumberInput,FileInput, Select



class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        fields = ('nom', 'description', 'prix', 'stock', 'categorie', 'images', 'vendeur')
        widgets = {
            'Nom': TextInput(attrs={
                'class': "form-control",
                # 'style': 'max-width: 300px;',
                'placeholder': 'Nom'
                }),
            'description': TextInput(attrs={
                'class': "form-control", 
                # 'style': 'max-width: 300px;',
                'placeholder': 'description'
                }),
            'prix': NumberInput(attrs={
                'class': "form-control", 
               
                }),
            'stock': NumberInput(attrs={
                'class': "form-control", 
                'placeholder': 'Quantité en Stock'
                }),
            'images': FileInput(attrs={
                'class': "form-control", 
               
                }),
            'categorie': Select(attrs={
                'class': "form-control", 
               
                }),
            'vendeur': Select(attrs={
                'class': "form-control", 
               
                }),
        }
