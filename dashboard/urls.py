from django.urls import path

from . import views

urlpatterns = [
    # Authentification SuperAdmin
    path("login/", views.login_view, name="dashboard-login"),
    path("logout/", views.logout_view, name="dashboard-logout"),

    # Dashboard
    path("", views.home, name="dashboard-home"),
    path("vendors/", views.vendor_list, name="dashboard-vendors"),
    path("vendors/add/", views.vendor_create, name="dashboard-vendor-add"),
]

