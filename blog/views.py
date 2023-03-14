from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

class PostList(ListView): #LISTVIEW 블로그 글 리스트 보기 장고 내장 함수
    model = Post
    ordering = '-pk'

    # template_name = 'blog/index.html'

# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk') # Post.objects.all() post안에 모든 (객체)내용을 가져옴
#     # Post.objects.all().order_by('-pk') -pk 프라이머리 키 (id)의 역순으로 정렬
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )

class PostDetail(DetailView): # DetailView 상세보기 장고 내장 함수
    model = Post

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )