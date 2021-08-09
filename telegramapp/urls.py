from django.urls import path
import telegramapp.views as telegramapp_view

app_name = 'telegramapp'

urlpatterns = [
    path('<str:verify>/', telegramapp_view.main, name='index'),
]