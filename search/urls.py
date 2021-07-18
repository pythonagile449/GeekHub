from django.urls import path

from search import views as search

app_name = 'search'

urlpatterns = [
    path('', search.Search.as_view(), name='search'),
]
