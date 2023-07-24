from .models import Code    # , Comment
from django import forms
from django.db import models

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


# from .models import File


class UploadFileForm(forms.Form):
    author = forms.CharField(max_length=25, required=False)
    title = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        # model = File
        fields = ['author', 'title', 'description', 'file_field']

# ------------------
# New form Format
# ------------------
from django import forms
from .models import Container, Files, Codes

class ContainerForm(forms.Form):
    title = forms.CharField(max_length=255)
    author = forms.CharField(max_length=255, required=False)
    email = forms.EmailField()
    tags = forms.CharField(max_length=255, required=False)
    is_private = forms.BooleanField(required=False)
    class Meta:
        model = Container
        fields = ['title', 'author', 'email', 'tags', 'is_private']

# class FilesForm(forms.ModelForm):
#     class Meta:
#         model = Files
#         fields = ['link', 'type']
class FilesForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        # model = File
        fields = ['file_field']
class FilesForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        # model = File
        fields = ['file_field']
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     file_field = cleaned_data.get('file_field')

    #     if not file_field:
    #         body = cleaned_data.get('body')
    #         print(f'body is :{body}')
    #         if not body:
    #             raise forms.ValidationError("1.Either the 'file_field' or the 'body' field must be provided.")

    #     return cleaned_data
class CodesForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, max_length=1000, required=False)
    class Meta:
        # model = Codes
        fields = ['body']
    
# * check if body and file are empty