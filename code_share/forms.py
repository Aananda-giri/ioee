from .models import Code    # , Comment
from django import forms


class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('title', 'code', 'author', 'email', 'tags')
        #fields = ('name', 'email', 'body')

'''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
'''

class EmailForm(forms.Form):
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)