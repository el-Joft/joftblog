from django import forms
from posts.models import Post
from pagedown.widgets import PagedownWidget

# class HomeForm(forms.Form):
#     title = forms.CharField()
#     body = forms.CharField()



class HomeForm(forms.ModelForm):
    title = forms.CharField( widget = forms.TextInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'post title'
        }
    ))

    body = forms.CharField( widget =PagedownWidget(show_preview=False))

    # body = forms.CharField( widget = forms.TextInput(
    #      attrs = {
    #         'class': 'form-control',
    #         'placeholder': 'write an article'
    #     }
    # ))

    modified = forms.DateField(widget = forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = ('title', 'body','image', 'draft', 'modified')