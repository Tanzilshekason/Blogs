from django.db import models
from django.conf import settings
from django.utils import timezone
# from authuser.models import CustomUser  # or from users.models if that's your app name


class LivePost(models.Model):
    STATUS_CHOICES = (
        ('Ongoing', 'Ongoing'),
        ('Ended', 'Ended'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ongoing')
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Follow',
        related_name='followed_posts'
    )
    
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.stars for r in ratings) / ratings.count(), 1)
        return 0


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('LivePost', on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveIntegerField(default=0)  # 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent multiple ratings per user/post

# Add this method in your LivePost model
# @property
# def average_rating(self):
#     ratings = self.ratings.all()
#     if ratings.exists():
#         return round(sum(r.stars for r in ratings) / ratings.count(), 1)
#     return 0


class Comment(models.Model):
    post = models.ForeignKey(LivePost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient}'


class Follow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follows'
    )
    post = models.ForeignKey(
        'LivePost', on_delete=models.CASCADE, related_name='follower_relations'
    )
    created_at = models.DateTimeField(default=timezone.now)  # ✅ Add default value




# class Rating(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     post = models.ForeignKey('LivePost', on_delete=models.CASCADE, related_name='ratings')
#     value = models.PositiveSmallIntegerField()  # 1 to 5
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'post')  # Prevent multiple ratings by same user

#     def __str__(self):
#         return f"{self.user} rated {self.post} - {self.value}"
