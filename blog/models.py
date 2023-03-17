from django.db import models
from django.contrib.auth.models import User
import os

class Tag(models.Model): # 다 대 다 관계 해시태그
    name = models.CharField(max_length=50, unique=True) #varchar 똑같은 이름의 카테고리 생성불가 unique=True
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) # url 슬러그에 한글 사용 allow_unicode

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'



class Category(models.Model): # 1대 다 관계 카테고리
    name = models.CharField(max_length=50, unique=True) #varchar 똑같은 이름의 카테고리 생성불가 unique=True
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) # url 슬러그에 한글 사용 allow_unicode

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'categories'



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
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) #카테고리가 삭제가되도 글 삭제는 안됨 NULL로 표시하겠다

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}' # 글제목(id=primarykey) 글번호::작성자


    def get_absolute_url(self):
        return f'/blog/{self.pk}/' # localhost8000/blog/1 2 3 ...

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] # hi.csv hi.excel처럼 .을 구분해서 자름 hi csv처럼 그리고 -1로 제일 뒤에거 가져오기 csv,excel