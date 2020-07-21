from decimal import Decimal, ROUND_DOWN
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from app_common.common.pdf_util import PdfUtil
from datetime import datetime
from suitou.services.suitou_service import SuitouService
from suitou.forms.suitou_form import SuitouForm
from suitou.forms.suitou_form import SuitouDetailFormset
from urllib import parse
from datetime import datetime


class DeliveryNoteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        '''
        出納書PDFをダウンロードする
        '''
        params, fileName = self._retrieveSuitouData()
        # template = get_template('suitou/delivery_note_pdf.html')
        # html = template.render(params)
        pdf = PdfUtil.renderToPdf('suitou/delivery_note_pdf.html', params)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            # filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" % (fileName)

            if not request.GET.get("preview"):
                content = "attachment; filename=%s" % (fileName)

            response['Content-Disposition'] = content
            response.set_cookie('loading_finish_flg', '')
            return response

        return HttpResponse("Not found")

    def _retrieveSuitouData(self):
        suitouId = self.request.GET['suitou_id']
        # suitouId = 45
        totalPrice = 0
        service = SuitouService(self.request)
        suitou = service.retrieveSuitou(suitouId)

        if not suitou:
            messages.error(self.request, '出納情報の取得に失敗しました。')
            return redirect(reverse('suitou_list_view'))

        suitou = list(suitou)[0]
        detailList = [detail.__dict__ for detail in service.retrieveSuitouDetailList(suitouId)]

        # 合計金額を計算
        for detail in detailList:
            detail['item_total'] = detail.get('price') * detail.get('amount')
            totalPrice = totalPrice + detail.get('item_total')
        zeigaku = (Decimal(totalPrice) * Decimal('0.08')).quantize(Decimal('0'),
                                                                   rounding=ROUND_DOWN)  # TODO: 税額計算を共通化
        suitou['total_price'] = totalPrice
        suitou['zeigaku'] = zeigaku
        suitou['zeikomi_total_price'] = zeigaku + totalPrice

        params = {
            'suitou': suitou,
            'detailList': detailList,
        }

        # ファイル名：例）出納書_20190706_株式会社〇〇〇〇.pdf
        fileName = parse.quote(
            f'出納書_{suitou["suitou_date"].strftime("%Y%m%d")}_{suitou["suitousaki"]}.pdf')

        return params, fileName
