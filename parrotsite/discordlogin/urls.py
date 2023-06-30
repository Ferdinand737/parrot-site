from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("discord_login", views.discord_login, name="discord_login"),
    path("login/redirect", views.login_redirect, name="login_redirect"),
    path("user_page/<int:user_id>/",views.user_page,name="user_page")
]