import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from insta.forms import PostForm, CommentForm
from insta.models import Tag, Post


@login_required
def index(request):
    timesince = timezone.now() - datetime.timedelta(days=3)
    post_list = (
        Post.objects.all()
        .filter(Q(author=request.user) | Q(author__in=request.user.following_set.all()))
        .filter(created_at__gte=timesince)
    )

    suggested_user_list = (
        get_user_model()
        .objects.all()
        .exclude(pk=request.user.pk)
        .exclude(pk__in=request.user.following_set.all())[:3]  # 처음 3명만 보이게 합니다.
    )
    comment_form = CommentForm()

    return render(
        request,
        "insta/index.html",
        {
            "post_list": post_list,
            "suggested_user_list": suggested_user_list,
            "comment_form": comment_form,
        },
    )


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
    comment_form = CommentForm()
    return render(
        request, "insta/post_detail.html", {"post": post, "comment_form": comment_form}
    )


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"포스팅#{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅#{post.pk} 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return render(
                    request,
                    "insta/_comment.html",
                    {
                        "comment": comment,
                    },
                )

            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "insta/comment_form.html", {"form": form})


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()  # 실제 DB에 count 쿼리를 던집니다.

    if (
        request.user.is_authenticated
    ):  # 로그인이 되어있으면 User객체, 로그인이 되어있지 않다면 AnonymousUser입니다.
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    return render(
        request,
        "insta/user_page.html",
        {
            "page_user": page_user,
            "post_list": post_list,
            "post_list_count": post_list_count,
            "is_follow": is_follow,
        },
    )
