from django.urls import path

from . import views

urlpatterns = [
    # Authentification SuperAdmin
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logOutUser, name="dashboard-logout"),

    # Dashboard
    path("", views.home, name="home"),
    path("vendeurs-filtre/", views.vendeurListFiltre, name="vendeurs-filtre"),
    path("vendeurs/", views.vendeur_list, name="vendeurs"),
    path("add-vendeur/", views.vendeur_create, name="add-vendeur"),
    path("block-vendeur/<int:pk>/", views.blocVendeur, name="block-vendeur"),
    path('debloc-vendeur/<int:pk>',  views.deblocVendeur, name="unblock-vendeur"),
    path('details-vendeur/<int:pk>',views.detailsVendeur, name="details-vendeur"),
    path('delete-vendeur/<int:pk>',  views.deleteVendeur, name="delete-vendeur"),
    path('update-vendeur/<int:pk>', views.updateVendeur, name="update-vendeur"),
    path("categories/", views.categoryList, name="categories"),
    path("categories/add/", views.addCategory, name="dashboard-category-add"),
    path("categories/update/<int:pk>/", views.updateCategory, name="dashboard-category-update"),
    path("categories/delete/<int:pk>/", views.deleteCategory, name="dashboard-category-delete"),

    # Articles / Produits
    path("articles/", views.articleList, name="articles"),
    path("articles/add/", views.addArticle, name="dashboard-article-add"),
    path("articles/update/<int:pk>/", views.updateArticle, name="dashboard-article-update"),
    path("articles/delete/<int:pk>/", views.deleteArticle, name="dashboard-article-delete"),
]
