from django import forms
from tinymce.widgets import TinyMCE
from .models import *


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail',
                  'categories')


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Leave your Comment',
                'class': 'form-control',
                'rows': '4',
                'cols': '10',
                'required': True,

            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Full Name e.g. Jason Doe',
                'class': 'form-control',
                'required': True,
                'name': 'name',


            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email Address e.g. Jason@email.com',
                'class': 'form-control',
                'name': 'email',
                'required': True,


            }
        )
    )

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')
