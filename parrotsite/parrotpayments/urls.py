from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("discord_login", views.discord_login, name="discord_login"),
    path("login/redirect", views.login_redirect, name="login_redirect"),
    path("user_page/<int:user_id>/",views.user_page,name="user_page"),
    path("user_page/<int:user_id>/<str:purchase_status>",views.user_page,name="user_page"),
    path("logout", views.logout_view, name="logout"),
    path("payments/checkout/<int:product_id>", views.create_checkout_session_view, name="create_checkout_session_view"),
    path("webhooks/stripe", views.stripe_webhook, name="stripe_webhook"),
]