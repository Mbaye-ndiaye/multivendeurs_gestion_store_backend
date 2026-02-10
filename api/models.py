from django.db import models
from django.utils import timezone

# Create your models here.


class Vendor(models.Model):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, unique=True)
    shop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vendeur"
        verbose_name_plural = "Vendeurs"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.shop_name}"
