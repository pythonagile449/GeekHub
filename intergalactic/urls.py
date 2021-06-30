from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views

from mainapp.views_mde import markdown_uploader

urlpatterns = [
    path('', include('mainapp.urls', namespace='mainapp')),
    path('admin/', admin.site.urls),
    path('auth/', include('usersapp.urls', namespace='usersapp')),

    # mardown editor urls
    path('martor/', include('martor.urls')),
    path('api/uploader/', markdown_uploader, name='markdown_uploader_page'),
    # ckeditor urls    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
