from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from insta.forms import PostForm
from insta.models import Tag, Post


@login_required
def index(request):
    return render(request, "insta/index.html", {})


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
            return redirect(post)  # TODO: get_absolute_url 활용
    else:
        form = PostForm()

    return render(
        request,
        "insta/post_form.html",
        {
            "form": form,
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "insta/post_detail.html", {"post": post})


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()  # 실제 DB에 count 쿼리를 던집니다.
    return render(
        request,
        "insta/user_page.html",
        {
            "page_user": page_user,
            "post_list": post_list,
            "post_list_count": post_list_count,
        },
    )
