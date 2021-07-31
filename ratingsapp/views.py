import json
from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache

from ratingsapp.models import RatingCount


class RatingsView(View):
    model = None  # Модель данных - Статьи или Комментарии  (data model - an article or a commentary)
    vote_type = None  # Тип комментария Like/Dislike        (like or dislike)

    @never_cache
    def post(self, request, pk):
        if request.POST.get('obj_id'):
            pk = request.POST['obj_id']
        obj = self.model.objects.get(pk=pk)
        if request.user == obj.author:
            return HttpResponse(
                json.dumps({
                    "result": True,
                    "positive": obj.rating.positive().count(),
                    "negative": obj.rating.negative().count(),
                    "total": obj.rating.total(),
                    "access_denied": '<h6-1>Запрещено оценивать самого себя! Голос не засчитан!</h6-1>',
                }),
                content_type="application/json"
            )
        try:
            rating = RatingCount.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                             users=request.user)
            if rating.rate is not self.vote_type:
                rating.rate = self.vote_type
                rating.save(update_fields=['rate'])
                result = True
            else:
                rating.delete()
                rating = 0
                result = False
        except RatingCount.DoesNotExist:
            rating = obj.rating.create(users=request.user, rate=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "positive": obj.rating.positive().count(),
                "negative": obj.rating.negative().count(),
                "total": obj.rating.total(),
                'user_chose': rating.rate if rating != 0 else 0,
            }),
            content_type="application/json"
        )
