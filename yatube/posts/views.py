from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect


from .models import Post, Group, User
from .forms import CommentForm, PostForm


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_list(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = Post.objects.filter(author=user).count()
    posts_numbers = post_list.count()

    context = {
        'author': user,
        'posts_list': post_list,
        'posts_count': posts_count,
        'page_obj': page_obj,
        'posts_numbers': posts_numbers,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    author = post.author
    context = {
        'author': author,
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    request.method == 'POST'
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
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
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.pk)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = post.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post.pk)

    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post,
    }

    return render(request, 'posts/post_create.html', context)
