from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='afficher_quantite')
def afficher_quantite(value):
    if value is None:
        return ''
    if isinstance(value, (int, float, Decimal)) and value == int(value):
        return int(value)
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return value
