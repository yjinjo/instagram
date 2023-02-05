from django.contrib import messages
from django.contrib.auth.views import LoginView, logout_then_login
from django.shortcuts import render, redirect
from .forms import SingupForm


login = LoginView.as_view(template_name="accounts/login_form.html")


def logout(request):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            messages.success(request, "Welcome to instagram")
            signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천(비동기 방식)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
    else:
        form = SingupForm()

    return render(
        request,
        "accounts/signup_form.html",
        {
            "form": form,
        },
    )
