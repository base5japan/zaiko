from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from suitou.services.suitou_service import SuitouService
from suitou.forms.suitou_form import SuitouForm
# from suitou.forms.suitou_form import SuitouFormset
from suitou.forms.suitou_form import SuitouDetailFormset
from app_table.models import SuitouDetail


class SuitouRegistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        '''
        出納登録画面-初期表示処理
        '''
        service = SuitouService(self.request)
        form = SuitouForm()
        formset = SuitouDetailFormset(None, queryset=SuitouDetail.objects.none())

        params = {
            'mode': 'regist',
            'form': form,
            'formset': formset,
            'shohin_json': service.retrieveShohin(),
            'company_json': service.retrieveCompany(),
        }

        return render(request, 'suitou/regist.html', params)

    def post(self, request, *args, **kwargs):
        '''
        出納登録画面-登録処理
        '''
        service = SuitouService(self.request)
        form = SuitouForm(request.POST)
        detailFormset = SuitouDetailFormset(request.POST)

        if (not form.is_valid()) or (not detailFormset.is_valid()):
            params = {
                'mode': 'regist',
                'form': form,
                'formset': detailFormset,
                'shohin_json': service.retrieveShohin(),
                'company_json': service.retrieveCompany(),
            }
            return render(request, 'suitou/regist.html', params)

        # 出納を登録する
        service.registCompany(form.cleaned_data['suitousaki'])
        service.registSuitou(form, detailFormset)
        messages.success(request, '出納情報を登録しました。')

        # 出納登録画面初期表示処理へリダイレクト
        return redirect(reverse('suitou_list_view'))
