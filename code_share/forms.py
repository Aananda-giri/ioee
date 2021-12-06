from .models import ToyComment, Comment
from django import forms


class ToyCommentForm(forms.ModelForm):
    class Meta:
        model = ToyComment
        fields = ('author', 'comment')
        #fields = ('name', 'email', 'body')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

