from django.urls import path
from posts.views import HomeView, PostListView
from . import views



app_name = 'posts'

urlpatterns =[
    path('', HomeView.as_view(), name = 'home' ),
    #path('<slug:slug>/', PostDetailView.as_view(), name = 'post_detail' ),
    path('<slug:slug>/', views.postDetail, name = 'post_detail' ),
    path('list', PostListView.as_view(), name='post_list'),
    path('edit/<slug:slug>/', views.editPost, name = 'edit_post'),
    path('delete/<slug:slug>/', views.deletePost, name = 'delete_post'),

]