from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usersapp.models import GeekHubUser


class CustomUserAdmin(UserAdmin):
    """
    Расширяем модель UserAdmin
    fieldsets: исходный набор полей формы
    *UserAdmin.fieldsets: добавляем расширенный набор полей формы,
        тип: кортеж содержащий ('заголовок группы по вашему выбору', {словарь c новыми полями})
    """
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Данные для активации',
            {
                'fields': (
                    'activate_key', 'activate_key_expires',
                ),
            },
        ),
        (
            'Профиль',
            {
                'fields': (
                    'profile_photo', 'birthday', 'user_information', 'gender',
                ),
            },
        ),
    )


admin.site.register(GeekHubUser, CustomUserAdmin)
