from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<str:category>', views.CategoryView.as_view(), name='category'),
    path('article/<int:pk>/', views.ArticleView.as_view(), name='article'),
]
