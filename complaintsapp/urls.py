from django.urls import path

from complaintsapp import views as complaint

app_name = 'complaints'

urlpatterns = [
    path('create/', complaint.CreateComplaintView.as_view(), name='create_complaint'),
    path('user_complaints_list/', complaint.ComplaintsListView.as_view(), name='complaints_list'),
    path('discard_complaint/<pk>/', complaint.ComplaintDiscardView.as_view(), name='discard_complaint'),
    path('approve_copmlaint/<pk>/', complaint.ComplaintApproveView.as_view(), name='approve_complaint'),
    path('complaint_detail/<pk>/<complaint_sender>', complaint.ComplaintDetailView.as_view(),
         name='complaint_detail'),
]
