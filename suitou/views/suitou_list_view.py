from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from suitou.services.suitou_service import SuitouService


class SuitouListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        '''
        納品一覧画面-初期表示処理
        '''
        mode = self.kwargs.get('mode')
        service = SuitouService(self.request)
        params = {
            'suitou_list': service.retrieveSuitouList(),
            'mode': mode,
        }

        return render(request, 'suitou/list.html', params)
