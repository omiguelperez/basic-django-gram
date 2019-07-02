"""Post forms."""

from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    """Post model form."""

    class Meta:
        """Meta class."""

        model = Post
        fields = ('user', 'profile', 'title', 'photo')
