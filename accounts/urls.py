from django.urls import path
from . import views



app_name = 'accounts'

urlpatterns =[
    
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    #path('edit/<slug:slug>/', views.editPost, name = 'edit_post'),
    #path('delete/<slug:slug>/', views.deletePost, name = 'delete_post'),

]