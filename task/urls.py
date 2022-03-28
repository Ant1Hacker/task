from django.contrib import admin
from django.urls import path

from accounts import views

admin.site.site_header = 'HR'

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # home
    path('', views.home, name='home'),
    # user
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('edit', views.edit, name='edit'),
    # pdf
    path('me', views.user_pdf, name='me'),
    # links
    path('links/<pk>', views.links, name='links'),
    path('link/add', views.link_add, name='link_add'),
    path('link/remove/<pk>', views.link_remove, name='link_remove'),
    # statuses
    path('statuses/<pk>', views.statuses, name='statuses'),
    path('status/add', views.status_add, name='status_add'),
    path('status/remove/<pk>', views.status_remove, name='status_remove'),
]
