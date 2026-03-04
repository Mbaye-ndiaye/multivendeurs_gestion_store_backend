from django import forms

from api.models import *


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'vendeur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
            'vendeur': forms.Select(attrs={'class': 'form-control'}),
        }


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'stock', 'type', 'categorie', 'vendeur', 'seuil', 'cout_de_revient']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité en stock', 'step': '0.01'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'vendeur': forms.Select(attrs={'class': 'form-control'}),
            'seuil': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seuil d\'alerte'}),
            'cout_de_revient': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Coût de revient', 'step': '0.01'}),
        }


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

