from django import forms
from .models import Post
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {
            'text': 'Комментарий',
        }
        fields = ('text', )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        labels = {
            'text': ('Текст поста'),
            'group': ('Группа поста')
        }
        fields = ('text', 'group', )
