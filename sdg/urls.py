from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("AddArticle", views.add_article, name="AddArticle"),
    path("AddProject", views.add_project, name="AddProject"),
    path("categories", views.categories, name="categories"),
    
    # API urls
    path("category_view/<str:category_name>", views.category_view, name="category_view"),
    path("article/<int:article_id>", views.article_view, name = "article_view"),
    path("markProject", views.mark_project, name="markProject")
]