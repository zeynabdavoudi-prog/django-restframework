from django import forms
from .models import Post


# just for test
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'context', 'category', 'status', 'published_date']
