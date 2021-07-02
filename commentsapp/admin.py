from django.contrib import admin
from commentsapp.models import CommentsBranch, LikeArticle, LikeComments

# Register your models here.


admin.site.register(CommentsBranch)
admin.site.register(LikeArticle)
admin.site.register(LikeComments)
