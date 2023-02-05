from django.urls import path

from accounts import views

urlpatterns = [
    path("login/", views.login, name="login"),  # /accounts/login/ => seetings.LOGIN_URL
    path("logout/", views.logout, name="logout"),
    path(
        "password_change/",
        views.password_change,
        name="password_change",
    ),
    path("signup/", views.signup, name="signup"),
    path("edit/", views.profile_edit, name="profile_edit"),
]
