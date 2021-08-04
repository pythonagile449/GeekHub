from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView

from commentsapp.models import CommentsBranch
from complaintsapp.models import Complaint
from mainapp.models import Article
from mainapp.views import ArticleDetail
from notifyapp.models import NotificationFactory
from usersapp.models import GeekHubUser


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
            queryset = Complaint.objects.filter(status='M')
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
    success_url = reverse_lazy('complaints:complaints_list')

    def delete(self, request, *args, **kwargs):
        complaint = self.get_object()
        if request.user.is_staff:
            reason = self.request.POST.get('reason')
            complaint.set_discard_status(reason)
            NotificationFactory.notify(request.user, complaint.sender, 'Жалоба отклонена', complaint)
            return HttpResponseRedirect(self.success_url)
        elif not request.user.is_staff and (request.user == complaint.sender):
            complaint.delete()
            return HttpResponseRedirect(self.success_url)

        response = HttpResponse()
        response.status_code = 403
        return response

    def get_context_data(self, **kwargs):
        context = super(ComplaintDiscardView, self).get_context_data()
        context['complaint_sender'] = self.get_object().sender
        return context


class ComplaintApproveView(ComplaintDiscardView):
    template_name = 'complaintsapp/complaint_confirm_approve.html'

    def delete(self, request, *args, **kwargs):
        if request.user.is_staff:
            complaint = self.get_object()
            complaint.set_approve_status()
            complaint_target_type = ContentType.objects.get(pk=complaint.content_type.pk)
            obj = complaint_target_type.get_object_for_this_type(pk=complaint.object_id)
            if complaint_target_type.model == 'article':
                obj.set_draft_status()
                NotificationFactory.notify(request.user, obj.author,
                                           'Статья снята с публикации в связи с жалобой', obj)
            NotificationFactory.notify(request.user, complaint.sender, 'Жалоба принята', complaint)
            return HttpResponseRedirect(self.success_url)
        response = HttpResponse()
        response.status_code = 403
        return response


class ComplaintDetailView(LoginRequiredMixin, ArticleDetail):
    template_name = 'complaintsapp/complaint_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ComplaintDetailView, self).get_context_data()
        context['title'] = 'Просмотр жалобы'
        complaint_sender = self.kwargs['complaint_sender']
        content_type = ContentType.objects.get_for_model(self.object)
        context['complaint_sender'] = GeekHubUser.objects.get(pk=complaint_sender)
        complaints = Complaint.objects.filter(sender=complaint_sender,
                                              content_type=content_type,
                                              object_id=self.object.pk, )
        context['complaints'] = complaints.filter(status='M') if self.request.user.is_staff else complaints
        return context
