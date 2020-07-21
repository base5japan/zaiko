from django.urls import path
from .views.suitou_list_view import SuitouListView
from .views.suitou_regist_view import SuitouRegistView
from .views.suitou_update_view import SuitouUpdateView
from .views.suitou_delete_view import SuitouDeleteView
from .views.delivery_note_view import DeliveryNoteView

urlpatterns = [
    path('list/', SuitouListView.as_view(), kwargs={'mode': 'list'}, name='suitou_list_view'),
    path('delivery_note_list/', SuitouListView.as_view(),
         kwargs={'mode': 'pdf_list'}, name='suitou_list_view_deivery_note'),
    path('regist/', SuitouRegistView.as_view(), name='suitou_regist_view'),
    path('delete/', SuitouDeleteView.as_view(), name='suitou_delete_view'),
    path('update/', SuitouUpdateView.as_view(), name='suitou_update_view'),
    path('delivery_note/', DeliveryNoteView.as_view(), name='delivery_note_view'),
]
