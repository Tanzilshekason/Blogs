from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LivePost, Comment
from .forms import LivePostForm, CommentForm
from django.core.paginator import Paginator


def home(request):
    return render(request, 'base.html')


def blog_list(request):
    posts = LivePost.objects.order_by('-created_at')
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_list.html', {'page_obj': page_obj})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = LivePostForm(request.POST, request.FILES,)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_list')
    else:
        form = LivePostForm()
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_update(request, pk):
    post = get_object_or_404(LivePost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = LivePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = LivePostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(LivePost, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'post': post})


# View for comments
@login_required
def post_detail(request, pk):
    post = get_object_or_404(LivePost, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        return redirect('post_detail', pk=pk)
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })
