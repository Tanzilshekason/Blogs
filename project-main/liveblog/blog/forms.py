from django import forms
from .models import LivePost, Comment

class LivePostForm(forms.ModelForm):
    class Meta:
        model = LivePost
        fields = ['title', 'content', 'image', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']