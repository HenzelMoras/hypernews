from django.urls import path, re_path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.ComingSoonPageView.as_view()),
    re_path(r'news/$', views.MainPageView.as_view()),
    re_path(r'news/\d+/', views.NewsView.as_view()),
    re_path(r'news/create/', views.CreateNewsView.as_view()),
]
