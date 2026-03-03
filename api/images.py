"""
"""
from api.models import Image
from api.serializers import ImageSerializer


def get_images(array_images):
    """
    Crée des objets Image pour chaque fichier et retourne la liste des ids.
    Utilisé pour associer des images à un Produit (item.images.add(id)).
    """
    ids = []
    for img_file in array_images:
        ser = ImageSerializer(data={"image": img_file})
        if ser.is_valid():
            ser.save()
            ids.append(ser.data["id"])
    return ids
