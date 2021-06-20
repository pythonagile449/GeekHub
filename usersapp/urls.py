from django.urls import path
import usersapp.views as users_view

app_name = 'usersapp'

urlpatterns = [
    path('', users_view.main, name='index'),
    path('login/', users_view.AuthenticationView.as_view(), name='login'),
    path('logout/', users_view.UserLogoutView.as_view(), name='logout'),
    path('registration/', users_view.RegistrationView.as_view(), name='registration'),
    path('account/<int:pk>', users_view.UserAccountView.as_view(), name='account'),
    path('edit/<int:pk>', users_view.UserAccountEdit.as_view(), name='modify'),
    path('delete/<int:pk>', users_view.UserAccountDeleteView.as_view(), name='delete'),
    path('verify/<email>/<activate_key>/', users_view.verify, name='verify'),
]
