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
]

