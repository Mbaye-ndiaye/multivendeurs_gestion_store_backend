from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Ancienne configuration (créait une récursion infinie en incluant api.urls dans lui‑même)
# from django.urls import path, include
# urlpatterns = [
#     path('api/', include('api.urls')),
# ]
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT,
#     )

# Pour l’instant, on laisse l’API sans routes spécifiques.
# Tu pourras ajouter tes endpoints ici plus tard, par exemple :
# from . import views
# urlpatterns = [
#     path('vendors/', views.vendor_list_api, name='api-vendors'),
# ]
urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
