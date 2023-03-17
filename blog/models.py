from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d", blank=True)
    file_upload = models.FileField(upload_to="blog/files/%Y/%m/%d", blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}' # 글제목(id=primarykey) 글번호::작성자


    def get_absolute_url(self):
        return f'/blog/{self.pk}/' # localhost8000/blog/1 2 3 ...

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] # hi.csv hi.excel처럼 .을 구분해서 자름 hi csv처럼 그리고 -1로 제일 뒤에거 가져오기 csv,excel