from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',) # 뒤에 , 붙이면 뒤에거는 안 쓰겠다