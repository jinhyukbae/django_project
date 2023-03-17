from django.shortcuts import render, redirect #   redirect url을 재지정 해줌
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied

class PostList(ListView): #LISTVIEW 블로그 글 리스트 보기 장고 내장 함수
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

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

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user # 글 작성(request)하는 유저 표기
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # authenticated 인증된 사용자냐? true false staff권한 or superuser 권한
            form.instance.author = current_user # form 객체에 작성자로 넣겠다
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str') # 수정 요청(request)을 post 방식으로
            # #post_form에 tags_str id 태그 요소인 애들 가져옴
            if tags_str:
                tags_str = tags_str.strip() # 한칸씩 띄면서 쓰인 것들을 잘라서 가져옴 가져옴 #감자 #고구마 #배우

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    # 태그랑 태그 생성여부 리턴
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response

        else:
            return redirect('/blog/')



class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload', 'category']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists(): #object 태그가 존재하면
            tags_str_list = list() # 태그가 담길 리스트를 생성
            for t in self.object.tags.all():
                tags_str_list.append(t.name) # 차례차례로 바인드
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            # 로그인된 상태 and request.user가 작성자냐 ==
            return super(PostUpdate, self).dispatch(request, *args, **kwargs) # dispatch get이냐 post냐를 구분
        # postupdate를 할 수 있는 권한 부여
        else:
            # 아니면 permissiondenied
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )

def tag_page(request, slug):
        tag = Tag.objects.get(slug=slug)
        post_list = tag.post_set.all()

        return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )