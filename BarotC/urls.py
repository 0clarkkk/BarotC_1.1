from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('admin_login', admin_login, name="admin_login"),
    path('admin_home', admin_home, name="admin_home"),
    path('user_login', user_login, name="user_login"),
    path('recruiter_login', recruiter_login, name="recruiter_login"),
    path('recruiter_signup', recruiter_signup, name="recruiter_signup"),
    path('user_signup', user_signup, name="user_signup"),
    path('user_home', user_home, name="user_home"),
    path('Logout', Logout, name="Logout"),
    path('view_users', view_users, name="view_users"),
    path('delete_user/<int:pid>', delete_user, name="delete_user"),
    
    path('change_password', change_password, name='change_password'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
