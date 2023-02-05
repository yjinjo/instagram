from django.urls import path

from accounts import views

urlpatterns = [
    path("login/", views.login, name="login"),  # /accounts/login/ => seetings.LOGIN_URL
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
]
