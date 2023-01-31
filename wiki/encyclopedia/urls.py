from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display, name = "display"),
    path("search/", views.search, name = "search"),
    path("new/", views.new, name="new"),
    path("save/", views.save, name="save"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random/", views.random, name="random"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("login_auth/", views.login_auth, name="login_auth"),
    path("register_auth/", views.register_auth, name="register_auth"),
    path("logout_view/", views.logout_view, name="logout_view"),
    path("home/",views.home, name="home"),
]
