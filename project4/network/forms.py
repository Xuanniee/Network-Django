from django import forms

from .models import Post, PostComment

# Django Form for New Post. Use ModelForm as we will be interacting with our Database.
class NewPost(forms.ModelForm):
    posting_area = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
               "resize": "none",
               "size": "auto",
               "placeholder": "What are your thoughts?",
               "class": "form-control"
            }
        )
    )
    class Meta:
        model = Post
        fields = ['posting_area']

# Comment
class NewPostComment(forms.ModelForm):
    comment_area = forms.CharField(
        label="Comment here!!",
        widget=forms.Textarea(
            attrs={
                "resize": "none",
                "size": "auto",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = PostComment
        fields = ['comment_area']