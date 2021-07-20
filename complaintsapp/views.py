from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, ListView

from commentsapp.models import CommentsBranch
from complaintsapp.models import Complaint
from mainapp.models import Article


class CreateComplaintView(LoginRequiredMixin, View):
    model = Complaint
    instances = {
        'article': Article,
        'comment': CommentsBranch,
    }

    def get(self, request):
        """
        Create a complaint object depend request instance.
        Takes an arguments from ajax request: obj_id, message, instance.
        """
        if request.method == 'GET' and request.is_ajax():
            if request.path == '/complaint/create/':
                obj_id = request.GET.get('obj_id')
                obj = self.instances.get(request.GET.get('instance')).objects.get(id=obj_id)
                message = request.GET.get('message')

                Complaint.objects.create(
                    sender=request.user,
                    message=message,
                    object_id=obj_id,
                    content_type=ContentType.objects.get_for_model(obj),
                    content_object=obj,
                )

                return JsonResponse({'success': 'Жалоба успешно оправлена.'})

        response = JsonResponse({'error': 'Bad request'})
        response.status_code = 400
        return response


class ComplaintsListView(ListView):
    template_name = 'mainapp/user_articles_list_table.html'

    def get_queryset(self):
        queryset = Complaint.objects.filter()
        return queryset
