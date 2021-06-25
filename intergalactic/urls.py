from django.contrib import admin
from django.urls import path, include
from mainapp import views as mainapp

urlpatterns = [
    path('', include('mainapp.urls', namespace='mainapp')),
    path('hub/<hub_name>', mainapp.hubs, name='hubs'),
    path('admin/', admin.site.urls),
    path('auth/', include('usersapp.urls', namespace='usersapp')),
    path('martor/', include('martor.urls')),
]
