from django.contrib import admin
from .models import LivePost, Comment

# @admin.register(LivePost)
# class LivePostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
#     list_filter = ('status', 'created_at')
#     search_fields = ('title', 'content', 'author__username')

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'user', 'created_at')
#     search_fields = ('content', 'user__username', 'post__title')


from django.contrib import admin
from .models import LivePost, Comment, Notification,Rating

admin.site.register(LivePost)
admin.site.register(Comment)
admin.site.register(Notification)

admin.site.register(Rating)


# 6. TESTS (tests.py)

