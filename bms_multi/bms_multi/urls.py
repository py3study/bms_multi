"""bms_multi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path

from book import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #前端部分####################
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('reg/', views.reg),
    path('zhuce/', views.zhuce),
    path('zhuce_ajax/', views.zhuce_ajax),
    # path('test/', views.test),
    #后端部分###################
    #查看内容
    path('books/', views.books),
    path('books/see_publish/', views.see_publish),
    path('books/see_author/', views.see_author),
    #添加内容
    path('books/book_exists/', views.book_exists),
    path('books/add_book/', views.add_book),
    path('books/add_publish/', views.add_publish),
    path('books/add_author/', views.add_author),
    #管理内容
    path('books/manage_book/', views.manage_book),
    path('books/manage_publish/', views.manage_publish),
    path('books/manage_author/', views.manage_author),
    #删除内容
    re_path('books/delete_book/(?P<id>\d+)', views.delete_book),
    re_path('books/delete_publish/(?P<id>\d+)', views.delete_publish),
    re_path('books/delete_author/(?P<id>\d+)', views.delete_author),
    #修改内容
    re_path('books/modify_book/(?P<id>\d+)', views.modify_book),
    re_path('books/modify_publish/(?P<id>\d+)', views.modify_publish),
    re_path('books/modify_author/(?P<id>\d+)', views.modify_author),
]
