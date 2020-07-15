from django.forms import ModelForm
from blog.models import Post,Comment


class PostForm(ModelForm):
    class Meta:
        model =Post
        fields =['title','content','author','category']

class CommentForm(ModelForm):
    class Meta:
        model =Comment
        fields =['content',]