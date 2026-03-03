from django.contrib import admin
from .models import (
    User,
    Vendeur,
    Image,
    Promotion,
    Categorie,
    Produit,
    Variation,
)

admin.site.register(User)
admin.site.register(Vendeur)
admin.site.register(Image)
admin.site.register(Promotion)
admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Variation)
