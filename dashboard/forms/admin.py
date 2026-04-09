from api.models import *
from django import forms
from django.forms import ModelForm, TextInput, NumberInput,FileInput, Select


class AdminForm(ModelForm):

    class Meta:
        model = AdminUser
        fields = ['nom', 'prenom', 'telephone', 'email']

        widgets = {
            'nom': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Nom'
                }),

            'prenom': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 400px;',
                'placeholder': 'Prénom'
                }),

            'telephone': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 400px;',
                'placeholder': 'Numéro de téléphone'
                }),

            'email': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 400px;',
                'placeholder': 'Adresse email'
                }),

        }