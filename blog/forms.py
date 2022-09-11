from django import forms
from .models import Post


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', )
