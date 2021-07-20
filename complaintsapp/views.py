from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView

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


class ComplaintsListView(LoginRequiredMixin, ListView):
    template_name = 'complaintsapp/users_complaints_list_table.html'
    context_object_name = 'complaints'

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Complaint.objects.all()
        else:
            queryset = Complaint.objects.filter(sender=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ComplaintsListView, self).get_context_data()
        context['title'] = 'Мои жалобы'
        return context


class ComplaintDiscardView(LoginRequiredMixin, DeleteView):
    model = Complaint
    template_name = 'complaintsapp/complaint_confirm_discard.html'
    success_url = reverse_lazy('complaint:complaints_list')

    def delete(self, request, *args, **kwargs):
        complaint = self.get_object()
        complaint.set_discard_status()

    def get_context_data(self, **kwargs):
        context = super(ComplaintDiscardView, self).get_context_data()
        context['complaint_sender'] = self.get_object().sender
        return context
