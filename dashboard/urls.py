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
    path("vendeurs/bloc/<int:pk>/", views.bloc_vendeur, name="dashboard-vendeur-bloc"),
    path("vendeurs/debloc/<int:pk>/", views.debloc_vendeur, name="dashboard-vendeur-debloc"),

    path("categories/", views.category_list, name="dashboard-categories"),
    path("categories/add/", views.category_add, name="dashboard-category-add"),
    path("categories/update/<int:pk>/", views.category_update, name="dashboard-category-update"),
    path("categories/delete/<int:pk>/", views.category_delete, name="dashboard-category-delete"),

    # Articles / Produits
    path("articles/", views.article_list, name="dashboard-articles"),
    path("articles/add/", views.article_add, name="dashboard-article-add"),
    path("articles/update/<int:pk>/", views.article_update, name="dashboard-article-update"),
    path("articles/delete/<int:pk>/", views.article_delete, name="dashboard-article-delete"),
]

