from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
path('accounts/', include('django.contrib.auth.urls')),
path('profile/', views.profile, name='profile'),
path('profile/edit/', views.edit_profile, name='edit_profile'),
path('blog/', views.blog_list, name='blog_list'),
path('blog/<int:id>/', views.blog_detail, name='blog_detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)