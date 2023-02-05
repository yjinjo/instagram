from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from django.shortcuts import render, redirect
from .forms import SingupForm, ProfileForm

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
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 환영합니다.")
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


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정/저장했습니다.")
            return redirect("profile_edit")
    else:
        form = ProfileForm(instance=request.user)
    return render(
        request,
        "accounts/profile_edit_form.html",
        {
            "form": form,
        },
    )
