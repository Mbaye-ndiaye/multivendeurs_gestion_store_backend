from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('vendeurs/', views.VendeurAPIListView.as_view(), name='api-vendors-list'),
    path('vendeurs/<int:id>/', views.VendeurAPIView.as_view(), name='api-vendors-detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
