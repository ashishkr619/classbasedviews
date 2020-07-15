from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.urls import views as auth_views
from blog.views import PostDetail,PostCreate,PostList,PostUpdate,PostDelete,Dashboard,PostCategory


app_name='blog'

urlpatterns = [
    # path('',Home.as_view(),name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('',PostList.as_view(),name='home'),
    path('<int:pk>/',PostDetail.as_view(),name='detail'),
    path('category/<int:pk>/',PostCategory.as_view(),name='category'),
    path('create/',PostCreate.as_view(),name='create'),
    path('<int:pk>/edit/',PostUpdate.as_view(),name='edit'),
    path('<int:pk>/delete/',PostDelete.as_view(),name='delete'),
    path('dashboard/',Dashboard.as_view(),name='dashboard'),
]
