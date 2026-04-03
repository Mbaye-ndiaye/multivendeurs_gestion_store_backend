"""
Génération PDF des factures (même principe qu'Easymarket : template facturation.html + WeasyPrint).
"""
import logging
import os
from io import BytesIO

from django.conf import settings
from django.core.files import File
from django.template.loader import render_to_string

from api.utils import Utils

logger = logging.getLogger(__name__)


def generer_facture_pdf(facture):
    """
    Rend le HTML Easymarket-style, écrit le PDF dans facture.facture_pdf.
    Retourne True si succès, False sinon.
    Import WeasyPrint à l'intérieur : évite le crash au démarrage si libcairo absent (ex. Windows local).
    """
    try:
        from weasyprint import HTML, CSS
        from weasyprint.fonts import FontConfiguration
    except OSError as e:
        logger.warning(
            "WeasyPrint indisponible (souvent libcairo manquant sur Windows). PDF non généré : %s",
            e,
        )
        return False
    vendeur = facture.vendeur
    signature_data, logo_data = None, None
    date_facture_str = facture.date_facture.strftime("%d_%m_%Y")
    nom_de_la_boutique = Utils.clean_directory_name(vendeur.nom_de_la_boutique) or "boutique"

    if vendeur.signature:
        signature_data = Utils.image_field_to_data_uri(vendeur.signature)
    if vendeur.avatar:
        logo_data = Utils.image_field_to_data_uri(vendeur.avatar)

    html_content = render_to_string(
        "facturation.html",
        {
            "facture": facture,
            "date_facture": facture.date_facture.strftime("%d/%m/%Y"),
            "date_echeance": facture.date_echeance.strftime("%d/%m/%Y"),
            "signature_data": signature_data,
            "logo_data": logo_data,
        },
    )
    font_config = FontConfiguration()
    base_dir = getattr(settings, "BASE_DIR", ".")
    base_url = base_dir if isinstance(base_dir, str) else str(base_dir)
    html = HTML(string=html_content, base_url=base_url)
    css = CSS(
        string="@page { size: A3; margin: 1cm 2cm }",
        font_config=font_config,
    )
    file_name = f"facture_{nom_de_la_boutique}_{date_facture_str}_{facture.pk}.pdf"
    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        logger.error("MEDIA_ROOT non défini : impossible de générer le PDF.")
        return False
    os.makedirs(media_root, exist_ok=True)
    path_file = os.path.join(media_root, file_name)
    try:
        html.write_pdf(path_file, stylesheets=[css])
        with open(path_file, "rb") as f:
            data = f.read()
        facture.facture_pdf.save(file_name, File(BytesIO(data)), save=True)
    except Exception as e:
        logger.exception("Erreur génération PDF facture %s: %s", facture.pk, e)
        return False
    finally:
        try:
            if os.path.isfile(path_file):
                os.remove(path_file)
        except OSError:
            pass
    return True
