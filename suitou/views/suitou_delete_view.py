from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from suitou.services.suitou_service import SuitouService
from django.contrib.auth.mixins import LoginRequiredMixin


class SuitouDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        '''
        納品一覧画面-削除処理
        '''
        SuitouService(request).deleteSuitou(request.POST.get("suitou_id"))
        messages.success(request, '納品情報を削除しました。')
        return redirect(reverse('suitou_list_view'))
