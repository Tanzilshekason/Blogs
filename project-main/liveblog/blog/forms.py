from django import forms
from .models import LivePost

class LivePostForm(forms.ModelForm):
    class Meta:
        model = LivePost
        fields = ['title', 'content', 'image', 'status']

