from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from suitou.services.suitou_service import SuitouService
from suitou.forms.suitou_form import SuitouForm
from suitou.forms.suitou_form import SuitouDetailFormset
from app_table.models import SuitouDetail


class SuitouUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        '''
        納品更新画面-初期表示処理
        '''
        suitouId = request.GET['suitou_id']
        service = SuitouService(request)
        suitou = service.retrieveSuitou(suitouId)

        if not suitou:
            messages.error(request, '納品情報の取得に失敗しました。')
            return redirect(reverse('suitou_list_view'))

        form = SuitouForm(list(suitou)[0])
        formset = SuitouDetailFormset(None, queryset=service.retrieveSuitouDetailList(suitouId))

        params = {
            'mode': 'update',
            'form': form,
            'formset': formset,
            'shohin_json': service.retrieveShohin(),
            'company_json': service.retrieveCompany(),
            'update_suitou_id': suitouId,
        }

        return render(request, 'suitou/regist.html', params)

    def post(self, request, *args, **kwargs):
        '''
        納品更新画面-更新処理
        '''
        suitouId = request.POST['update_suitou_id']
        service = SuitouService(request)

        suitou = service.retrieveSuitouModel(suitouId)
        suitouDetails = service.retrieveSuitouDetailModelBySuitou(suitou)

        form = SuitouForm(request.POST, instance=suitou)
        formset = SuitouDetailFormset(request.POST, queryset=suitouDetails)

        if not form.is_valid() or not formset.is_valid():
            params = {
                'mode': 'update',
                'form': SuitouForm(request.POST),
                'formset': SuitouDetailFormset(request.POST),
                'shohin_json': service.retrieveShohin(),
                'company_json': service.retrieveCompany(),
                'update_suitou_id': suitouId,
            }
            return render(request, 'suitou/regist.html', params)

        # 納品を登録する
        service.updateSuitou(form, formset)
        service.registCompany(form.cleaned_data['suitousaki'])
        messages.success(request, '納品情報を更新しました。')

        # 納品一覧画面の初期表示処理へリダイレクト
        return redirect(reverse('suitou_list_view'))
