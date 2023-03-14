from django.urls import path
from . import views


urlpatterns = [
    # path('<int:pk>/', views.single_post_page), # int 타입의 pk데이터(id값) 127.0.0.1/8000/1, 2, 3 ...
    # path('', views.index),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]