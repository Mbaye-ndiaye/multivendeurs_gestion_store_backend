from django import forms

from api.models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "shop_name",
            "address",
            "country",
        ]

