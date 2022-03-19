from django.urls import path
from legal_map.articles import views

urlpatterns = (
    path('', views.IndexView.as_view(), name='index'),
    path('contact/', views.contact_us, name='contact us'),
    path('articles/', views.list_all_articles, name='list all articles'),
    path('articles/details/<int:pk>', views.article_details, name='article details'),
    path('articles/create/', views.create, name='article create'),
    path('articles/edit/<int:pk>', views.edit_article, name='article edit'),
    path('articles/delete/<int:pk>', views.delete_article, name='article delete'),
    path('articles/myarticles/', views.list_my_articles, name='list my articles'),
)
