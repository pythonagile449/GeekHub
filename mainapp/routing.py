from django.urls import path, include

from consumers import TopMenuConsumer

websocket_urlpatterns = [
    path('get-top-menu/<str:hub_name>', TopMenuConsumer.as_asgi(), name='top_menu_consumer'),
]