from django.urls import path

from . import views

urlpatterns = [
    # Authentification SuperAdmin
    path("login/", views.login_view, name="dashboard-login"),
    path("logout/", views.logout_view, name="dashboard-logout"),

    # Dashboard
    path("", views.home, name="dashboard-home"),
    path("vendeurs/", views.vendeur_list, name="dashboard-vendeurs"),
    path("vendeurs/add/", views.vendeur_create, name="dashboard-vendeur-add"),
    
    # Blocage/Déblocage des vendeurs
    path("vendeurs/bloc/<int:pk>/", views.bloc_vendeur, name="dashboard-vendeur-bloc"),
    path("vendeurs/debloc/<int:pk>/", views.debloc_vendeur, name="dashboard-vendeur-debloc"),
]

