from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SingupForm


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Welcome to instagram")
            return redirect("root")
    else:
        form = SingupForm()

    return render(
        request,
        "accounts/signup_form.html",
        {
            "form": form,
        },
    )
