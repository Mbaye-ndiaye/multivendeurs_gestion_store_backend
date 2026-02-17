from django import forms

from api.models import *



class VendorForm(forms.ModelForm):
    """
    Formulaire pour créer un vendeur (hérite de User).
    Adapté au nouveau modèle Vendor qui hérite de User.
    """
    class Meta:
        model = Vendeur
        fields = [
            "nom",
            "prenom",
            "email",
            "telephone",
            "adresse",
            "pays",
            "nom_de_la_boutique",
            # "couleur",
            "domaine",
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse'
            }),
            'pays': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pays'
            }),
            'nom_de_la_boutique': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la boutique'
            }),
            # 'couleur': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'type': 'color',
            #     'placeholder': 'Couleur'
            # }),
            'domaine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Domaine'
            }),
        }

