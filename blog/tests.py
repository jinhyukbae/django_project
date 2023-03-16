from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def navbar_test(self, soup):

        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        self.assertIn('Home', navbar.text)

        logo_btn = navbar.find('a', text='Blog') # a태그중에 텍스트가 blog 인거
        self.assertEqual(logo_btn.attrs['href'], '/') # attribute 속성이 href 인거 본문은 ./index.html 이므로 false 가 뜸
        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')
        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):
        response = self.client.get('/blog/') # localhost:8000/blog  : post_list.html

        self.assertEqual(response.status_code, 200) # status code가 200(사이트 접속이 잘되느냐)이면 true 404 page not found error ..

        soup = BeautifulSoup(response.content, 'html.parser') # soup로 태그 찾기 <br> 같은 것들

        self.assertEqual(soup.title.text, 'Blog') # <title></title>이 Blog면 true

        # navbar = soup.nav # soup에 <nav>
        # self.assertIn('Blog', navbar.text) # <nav> 안에 blog란 단어가 있으면 true
        # self.assertIn('About Me', navbar.text) # <nav> 안에 about me가 있으면 true
        # 위 코드를 아래처럼 줄일 수 있음
        self.navbar_test(soup)

        self.assertEqual(Post.objects.count(), 0) #포스팅 글의 개수(count) 가 0이면 true
        main_area = soup.find('div', id='main-area') # div 안에 있는 id 요소 값이 main-area 인 걸 찾기
        self.assertIn('아직 게시물이 없습니다', main_area.text) # main-area 에 아직 게시물이 없습니다가 있으면 true

        post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.',
        )

        post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
        )

        self.assertEqual(Post.objects.count(), 2) # 위에 두개의 글을 썼으므로 2=2 true

        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(response.status_code, 200)
        main_area = soup.find('div', id='main-area')

        self.assertIn(post_001.title, main_area.text) # main_area.text 안에 post_001.title이 있으면 true
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다', main_area.text) # 아직 게시물이 없습니다 라는 내용이 없으면 true

    def test_post_detail(self):
        # 0.   Post가 하나 있다.
        post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.',
        )
        # 0.1  그 포스트의 url은 'blog/1/' 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/') #url이 오른쪽이면 true

        # 1.   첫 번째 post의 detail 페이지 테스트
        # 1.1  첫 번째 post url로 접근하면 정상적으로 작동한다. (status code: 200)
        response = self.client.get(post_001.get_absolute_url()) # localhost:8000/blog/1, 2, 3
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser') # html 태그 가져오기 parser

        # 1.2  post_list 페이지와 똑같은 네비게이션 바가 있다.
        # navbar = soup.nav  # beautifulsoup를 이용하면 간단히 페이지의 태그 요소에 접근이 가능합니다.
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        # 위 코드를 아래처럼 줄일 수 있음
        self.navbar_test(soup)

        # 1.3  첫 번째 post의 title이 브라우저 탭에 표기되는 페이지 title에 있다.
        self.assertIn(post_001.title, soup.title.text)

        # 1.4  첫 번째 post의 title이 post-area에 있다.
        main_area = soup.find('div', id='main-area') # <div> 찾기
        post_area = main_area.find('div', id='post-area') # <div><div> 디비전 내부 디비전 찾기
        self.assertIn(post_001.title, post_area.text) # 왼쪽 내용이 오른쪽에 들어있느냐

        # 1.5  첫 번째 post의 작성자(author)가 post-area에 있다.
        # 아직 작성 불가

        # 1.6  첫 번째 post의 content가 post-area에 있다.
        self.assertIn(post_001.content, post_area.text)
