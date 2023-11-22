from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('profile', views.profileMain, name='profileMain'),
    path('register',views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('edit-profile', views.CreateOrUpdatePhotographerProfileView.as_view(), name='edit_profile'),
    path('search', views.search, name='search'),
    path('<str:name>', views.profile_detail, name='profile_detail'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)