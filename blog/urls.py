from django.urls import path
from . import views
app_name = "blog_app"
urlpatterns = [
    path('', views.index, name='home'),
    path('category/<slug:slug>/', views.blog_column, name='category'),

    path('post/<slug:slug>/', views.post, name='post-detail'),
    path('post/<id>/update/', views.post_update, name='post-update'),
    path('post/<id>/delete/', views.post_delete, name='post-delete'),
    path('create/', views.post_create, name='post-create'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),

]
