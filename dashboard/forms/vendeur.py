from api.models import *
from django import forms
from django.forms import ModelForm, TextInput, NumberInput,FileInput, Select


class VendeurForm(ModelForm):

    class Meta:
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
                
        #    'intech_api_key': TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Clé API Intech'
        #         }),
            
        #     'stripe_publishable_key': TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Clé publique Stripe'
        #         }),
        #     'stripe_secret_key': TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Clé secrète Stripe'
        #         }),
        #     'stripe_endpoint_secret': TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Endpoint secrète Stripe'
        #         }),
        #     'nb_vendeur_a_ajouter': NumberInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Nombre de vendeurs à ajouter'
        #         }),
        #     'wave_api_secret_key': TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Clé secrète Wave'
        #         }),
        #     'wave_api_key': TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Clé API Wave'
        #         }),
        #     'paygate_api_key': TextInput(attrs={
        #         'class': "form-control",
        #         'placeholder': 'Clé API Paygate'
        #         }),
        #     'stripe_is_set': Select(choices=[(True, 'Oui'), (False, 'Non')],attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 400px;',
        #         'placeholder': 'Stripe configuré',
        #      }),
        #     'wave_is_set': Select(choices=[(True, 'Oui'), (False, 'Non')],attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 400px;',
        #         'placeholder': 'Wave configuré',
        #      }),
        #     'paygate_is_set': Select(choices=[(True, 'Oui'), (False, 'Non')],attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 400px;',
        #         'placeholder': 'Paygate configuré',
        #      }),
        #     'paygate_network': Select(choices=[('FLOOZ', 'FLOOZ'), ('TMONEY', 'TMONEY')],attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 400px;',
        #         'placeholder': 'Réseau Paygate',
        #      }),
        }