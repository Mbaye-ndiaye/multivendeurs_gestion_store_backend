import base64
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Aligné sur backend_easymarket_multivendor (utilisé par dashboard.views)
REGEX = os.environ.get("regex")


class Utils:
    # pass

    @staticmethod
    def clean_directory_name(name):
        """Comme Easymarket : nom de fichier sans caractères spéciaux."""
        if not name:
            return "boutique"
        name = name.replace(" ", "-").lower()
        name = re.sub(r"[^\w\-]", "", name)
        return name[:200] or "boutique"

    @staticmethod
    def image_field_to_data_uri(field_file):
        """
        Convertit une ImageField en data URI (comme Easymarket : data:image/png;base64, ...).
        """
        if not field_file:
            return None
        try:
            path = field_file.path
        except Exception:
            return None
        if not path or not os.path.isfile(path):
            return None
        ext = os.path.splitext(path)[1].lower()
        mime = "image/png"
        if ext in (".jpg", ".jpeg"):
            mime = "image/jpeg"
        elif ext == ".gif":
            mime = "image/gif"
        elif ext == ".webp":
            mime = "image/webp"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64, {b64}"

    @staticmethod
    def translate_errors_array(serializer_errors):
        """Retourne les erreurs serializer telles quelles (traduction optionnelle)."""
        return serializer_errors
