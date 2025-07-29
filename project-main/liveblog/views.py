from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LivePost, Comment,Notification, Follow,Rating
from .forms import LivePostForm, CommentForm,RatingForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from authuser.models import CustomUser  # Adjust if needed
from django.contrib import messages
from django.http import HttpResponseForbidden


from django.db.models import Avg
from django.db.models import Q

# Notification.objects.create(
#     recipient=post_list.author,
#     message=f'{request.user.username} rated your post "{post.title}"'
# )
@login_required
def notification_list(request):
    notes = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notes})


@login_required
def rate_post(request, post_id):
    post = get_object_or_404(LivePost, id=post_id)
    score = int(request.POST.get('score'))
    Rating.objects.update_or_create(user=request.user, post=post, defaults={'score': score})
    return redirect('post_detail', pk=post.id)



from django.db.models import Q
from django.core.paginator import Paginator
from .models import LivePost, Follow

# @login_required
# def post_list(request):
#     query = request.GET.get('q')
#     status = request.GET.get('status')

#     posts = LivePost.objects.all()

#     if query:
#         posts = posts.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query)
#         )

#     if status:
#         posts = posts.filter(status=status)

#     paginator = Paginator(posts, 5)  # Show 5 posts per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # ✅ This is the key part: list of post IDs the user is following
#     followed_post_ids = Follow.objects.filter(user=request.user).values_list('post_id', flat=True)

#     return render(request, 'post_list.html', {
#         'posts': page_obj,
#         'query': query,
#         'status': status,
#         'followed_post_ids': list(followed_post_ids),  # 👈 Add to context
#     })

from .models import Rating, Follow

def post_list(request):
    ...
    posts = LivePost.objects.all()
    
    # search/filter logic (if any)
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    if query:
        posts = posts.filter(title__icontains=query)
    if status:
        posts = posts.filter(status=status)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # logged in user rating info
    user_rated_post_stars = {}
    if request.user.is_authenticated:
        ratings = Rating.objects.filter(user=request.user)
        user_rated_post_stars = {r.post_id: r.stars for r in ratings}
        followed_post_ids = Follow.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        followed_post_ids = []

    return render(request, 'post_list.html', {
        'posts': page_obj,
        'query': query,
        'status': status,
        'followed_post_ids': followed_post_ids,
        'user_rated_post_stars': user_rated_post_stars,
    })




@login_required
def post_create(request):
    form = LivePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_list')
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(LivePost, pk=pk)
    
    # Only allow author or staff to edit
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    form = LivePostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(LivePost, pk=pk)

    # Allow only the author or admin to delete
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'post_confirm_delete.html', {'post': post})


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



def create_comment_notification(comment):
    post = comment.post
    author = post.author
    if comment.user != author:
        Notification.objects.create(
            user=author,
            message=f"{comment.user.username} commented on your post '{post.title}'."
        )
        send_mail(
            subject="New Comment Notification",
            message=f"{comment.user.username} commented on your post '{post.title}'.",
            from_email=None,
            recipient_list=[author.email],
        )

def notify_followers(post):
    followers = post.follow_set.all()
    for follow in followers:
        Notification.objects.create(
            user=follow.user,
            message=f"The post '{post.title}' you follow has been updated."
        )

def notify_admins(message):
    admins = CustomUser.objects.filter(is_staff=True)
    for admin in admins:
        Notification.objects.create(user=admin, message=message)



@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notification_list.html', {'notifications': notifications})


@login_required
def follow_post(request, post_id):
    post = get_object_or_404(LivePost, id=post_id)
    Follow.objects.get_or_create(user=request.user, post=post)
    return redirect('post_list')

@login_required
def unfollow_post(request, post_id):
    post = get_object_or_404(LivePost, id=post_id)
    Follow.objects.filter(user=request.user, post=post).delete()
    return redirect('post_list')
# @login_required
# def unfollow_post(request, post_id):
#     post = get_object_or_404(LivePost, id=post_id)
#     Follow.objects.filter(user=request.user, post=post).delete()
#     return redirect('post_detail', pk=post_id)


# @login_required
# def followed_posts(request):
#     followed = Follow.objects.filter(user=request.user).select_related('post')
#     posts = [f.post for f in followed]
#     return render(request, 'followed_posts.html', {'posts': posts})

# @login_required
# def follow_post(request, post_id):
#     post = get_object_or_404(LivePost, id=post_id)
#     follow, created = Follow.objects.get_or_create(user=request.user, post=post)

#     if created and post.author != request.user:
#         Notification.objects.create(
#             user=post.author,
#             message=f"{request.user.username} followed your post: '{post.title}'"
#         )

#     return redirect('post_detail', pk=post_id)

from django.views.decorators.http import require_POST

@login_required
def rate_post(request, post_id):
    post = get_object_or_404(LivePost, id=post_id)
    rating, created = Rating.objects.get_or_create(post=post, user=request.user)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = RatingForm(instance=rating)

    return render(request, 'rate_post.html', {'form': form, 'post': post})
