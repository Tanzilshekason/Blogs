from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LivePost, Comment
from .forms import LivePostForm, CommentForm
from django.core.paginator import Paginator

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
from django.http import JsonResponse

def broadcast_post(post):
    channel_layer = get_channel_layer()
    html = render_to_string('post_card.html', {'post': post})
    async_to_sync(channel_layer.group_send)(
        "live_posts",
        {
            "type": "send_post",
            "data": {
                "html": html,
                "id": post.id,
                "author": post.author.username,
            },
        },
    )

def test_broadcast(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "live_posts",
        {
            "type": "send_post",
            "data": {"html": "<div>Test Post</div>", "id": 0},
        }
    )
    return JsonResponse({"status": "sent"})

def broadcast_delete(post_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "live_posts",
        {
            "type": "delete_post",
            "data": {
                "id": post_id,
            },
        },
    )



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
            broadcast_post(post)
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
            broadcast_post(post)
            return redirect('blog_list')
    else:
        form = LivePostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(LivePost, pk=pk, author=request.user)
    if request.method == 'POST':
        post_id = post.id
        post.delete()
        broadcast_delete(post_id)
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'post': post})






