

from api.models import *
from api.serializers import *


def get_images(array_images):
    return map(lambda x: serializerImage(x), array_images)


def serializerImage(image):
    imageSerializer = ImageSerializer(data={"image": image})
    if imageSerializer.is_valid():
        imageSerializer.save()
        return imageSerializer.data["id"]

def get_variation(array_items):
    variations = []
    quantite = 0
    for el in array_items:
        if "images[]" in el:
            for image in el.get("images[]"):
                imageSerializer = ImageSerializer(data={"picture": image})
                if imageSerializer.is_valid():
                    imageSerializer.save()
                    el['images'] = imageSerializer.data['id']

        variationSerializer = VariationSerializer(
            data={"taille": el.get('taille', None),
                  "couleur": el.get('couleur', None),
                  "quantite": el.get('quantite'),
                  "seuil": el.get('seuil'),
                  "active": el.get('active'),
                  "images": el.get('images')
                })
        if variationSerializer.is_valid():
            variationSerializer.save()
            variations.append(variationSerializer.data['id'])
            
    return variations

# def get_orderproduits(array_produits):
#     orderproduits = []
#     for el in array_produits:

#         orderproduitsSerializer = OrderItemSerializer(
#             data={
#                     "produit": el.get('produit'),
#                     "quantite": el.get('quantite'),
#                     "prix": el.get('prix'),
#                     "order": el.get('order'),
#                     "variations": el.get('variations',[])
#                 })
#         if orderproduitsSerializer.is_valid():
#             orderproduitsSerializer.save()
#             orderproduits.append(orderproduitsSerializer.data['id'])
            
       
#     return orderproduits


# def get_and_process_produits(request):
#     produits = []
#     if 'produits' in request.data and request.data['produits']:
#         produits = get_orderproduits(request.data.get('produits', []))
#     return produits
