from api.models import *
from django import forms
from django.forms import ModelChoiceField
from django.forms import ModelForm, TextInput, NumberInput,FileInput, Select


class VendeurUpdateForm(ModelForm):
    service = ModelChoiceField(queryset=Service.objects.all(), empty_label="Sélectionner un service")
    class Meta:
        TRUE_FALSE_CHOICES = (
        (True, 'True'),
        (False, 'False'),
        )
        model = Vendeur
        fields = ['nom', 'prenom', 'telephone', 'email','nom_de_la_boutique','couleur','domaine','devise','nb_vendeur_a_ajouter',]
        
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
            # 'password': TextInput(attrs={
            #     'class': "form-control", 
            #     # 'style': 'max-width: 300px;',
            #     'placeholder': 'Mot de passe'
            #     }),

            'nom_de_la_boutique': TextInput(attrs={
                'class': "form-control",
                
                'style': 'max-width: 400px;',
                'placeholder': 'Nom de la boutique'
                }),

            'couleur': TextInput(attrs={
                'class': "form-control",
                'type':'color',
                'style': 'max-width: 400px;',
                'placeholder': 'Couleur'
                }),

            'domaine': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Domaine'
                }),


            'service': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Service',
             }),
             'devise': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Devise',
             }),

             
            'nb_vendeur_a_ajouter': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'Nombre de vendeurs à ajouter'
            }),
            
            
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Récupérer l'ID du service du vendeur à partir des données initiales
        vendeur_service_id = self.instance.service.id if self.instance and self.instance.service else None
        # Définir la valeur initiale pour le champ service
        self.fields['service'].initial = vendeur_service_id
    
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Récupérer le service à partir du formulaire
        service = self.cleaned_data.get('service')

        if service:
            instance.service = service

        if commit:
            instance.save()

        return instance
    