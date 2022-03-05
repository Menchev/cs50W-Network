# all forms for the Network app
from django import forms

# form for adding a new post
class NewPostForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control mx-auto', 
            'rows': '3',
            }), 
            label="New Post")