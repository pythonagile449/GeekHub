import json
from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from ratingsapp.models import RatingCount


class RatingsView(View):
    model = None  # Модель данных - Статьи или Комментарии  (data model - an article or a commentary)
    vote_type = None  # Тип комментария Like/Dislike        (like or dislike)

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            rating = RatingCount.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                             users=request.user)
            if rating.rate is not self.vote_type:
                rating.rate = self.vote_type
                rating.save(update_fields=['rate'])
                result = True
            else:
                rating.delete()
                result = False
        except RatingCount.DoesNotExist:
            obj.rating.create(users=request.user, rate=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "positive": obj.rating.positive().count(),
                "negative": obj.rating.negative().count(),
                "total": obj.rating.total()
            }),
            content_type="application/json"
        )
