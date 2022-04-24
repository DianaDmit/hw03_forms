from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


from .models import Post, Group, User
from .forms import PostForm


User = get_user_model()


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    author_posts_numbers = post_list.count()
    page_obj = paginator.get_page(page_number)
    posts_count = Post.objects.filter(author=user).count()
    context = {
        'user': user,
        'posts_list': post_list,
        'posts_count': posts_count,
        'page_obj': page_obj,
        'author_posts_numbers': author_posts_numbers,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    author_posts = author.posts
    count_posts = author_posts.count()
    context = {
        'author': author,
        'title': post.text,
        'post': post,
        'count_posts': count_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', str(request.user))
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    username = str(request.user)
    author = get_object_or_404(User, username=username)
    if request.user.username != author.username:
        return redirect('posts:post_detail', post_id)
    post = get_object_or_404(Post, id=post_id, author=author)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if request.method == 'POST':
        if form.is_valid():
            post.save()
            return redirect('posts:post_detail', post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {'form': form,
                                                      'is_edit': True,
                                                      'post_id': post_id})
