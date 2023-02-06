from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from insta.forms import PostForm
from insta.models import Tag


# Create your views here.
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            # post.tag_set  # TODO
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect("/")  # TODO: get_absolute_url 활용
    else:
        form = PostForm()

    return render(
        request,
        "insta/post_form.html",
        {
            "form": form,
        },
    )
