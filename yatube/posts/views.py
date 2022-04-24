from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


from .models import Post, Group, Follow
from .forms import PostForm, CommentForm

date = 10
number = 10
User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
    paginator = Paginator(post_list, number)
    page_number = request.GET.get('page')
    page_obj =\
        paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post = author.post.select_related('group').all()
    paginator = Paginator(post, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    request.method == 'POST'
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/post_create.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=post.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if request.user == post.author:
        request.method == 'POST'
        form = PostForm(request.POST or None,
                        files=request.FILES or None, instance=post)
        if not form.is_valid():
            return render(request, 'posts/post_create.html',
                          {'form': form, 'is_edit': is_edit, 'post': post})
        post.save()
        return redirect('posts:post_detail', post.pk)
    return redirect('posts:post_detail', post.pk)
