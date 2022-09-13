from django import forms
from .models import Post, Comment


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('content', )

