from django import forms
from .models import LivePost, Comment, Rating

class LivePostForm(forms.ModelForm):
    class Meta:
        model = LivePost
        fields = ['title', 'content', 'image', 'video', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, f"{i} Stars") for i in range(1, 6)])
        }
