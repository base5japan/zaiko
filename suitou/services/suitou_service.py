from app_table.models import Suitou
from app_table.models import SuitouDetail
from app_table.models import Shohin
from app_table.models import Company
from decimal import Decimal, ROUND_DOWN
from datetime import datetime
from django.db.models import Sum
from django.db import connection
import json


class SuitouService:
    '''
    出納画面用サービスクラス
    '''

    def __init__(self, request):
        self.request = request

    def retrieveSuitou(self, suitouId):
        '''
        出納情報を検索する
        '''
        suitou = (Suitou.objects
                  .filter(belong_user=self.request.user.email, id=suitouId)
                  .values('id', 'suitou_date', 'suitousaki', 'total_price', 'memo')
                  )
        return suitou

    def retrieveSuitouDetailList(self, suitouId):
        '''
        出納情報を検索する
        '''
        suitouDetailList = (SuitouDetail.objects
                            .filter(belong_user=self.request.user.email, suitou_id=suitouId)
                            )
        return suitouDetailList

    def retrieveSuitouModel(self, suitouId):
        '''
        出納情報を検索する
        '''
        suitou = Suitou.objects.get(belong_user=self.request.user.email, id=suitouId)
        return suitou

    def retrieveSuitouDetailModelBySuitou(self, suitou):
        '''
        出納情報を検索する
        '''
        suitouDetail = SuitouDetail.objects.all().filter(
            belong_user=self.request.user.email,
            suitou=suitou
        )

        return suitouDetail

    def retrieveSuitouList(self):
        '''
        出納一覧情報を検索する
        '''
        # suitouList = (Suitou.objects
        #     .filter(belong_user=self.request.user.email)
        #     .values('id', 'suitou_date', 'suitousaki', 'total_price', 'memo')
        #     .values('id', 'suitou_date', 'suitousaki', 'memo')
        #     .order_by('-suitou_date', '-regist_date') # 降順
        #     .annotate(total_price = Sum('suitoudetail__price * suitoudetail__amount'))
        # )

        query = '''
            select
                n.id, n.suitou_date, n.suitousaki, n.memo, sum(d.price * d.amount) as zeinuki_total_price
            from 
                app_table_suitou as n
            left outer join
                app_table_suitoudetail as d
            on
                n.id = d.suitou_id
            where
                n.belong_user = %s
            group by
                n.id, n.suitou_date, n.suitousaki, n.memo
            order by
                n.suitou_date desc, n.regist_date desc
        '''

        def dictfetchall(cursor):
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        with connection.cursor() as cursor:
            cursor.execute(query, [self.request.user.email])
            suitouList = dictfetchall(cursor)

        for suitou in suitouList:
            if suitou.get('zeinuki_total_price'):
                suitou['total_price'] = (suitou.get('zeinuki_total_price') *
                                         Decimal('1.08')).quantize(Decimal('0'), rounding=ROUND_DOWN)
            else:
                suitou['total_price'] = Decimal('0')

        return suitouList

    def deleteSuitou(self, suitouId):
        '''
        出納情報を削除する
        '''
        suitou = Suitou.objects.get(belong_user=self.request.user.email, id=suitouId)
        suitou.delete()

    def retrieveShohin(self):
        '''
        登録画面で選択できる商品情報を検索する
        '''
        shohinJson = json.dumps(
            list(Shohin.objects
                 .filter(belong_user=self.request.user.email)
                 .values('kataban', 'shohin_name', 'zaikosu', 'price')
                 .order_by('kataban')
                 )
        )
        return shohinJson

    def retrieveCompany(self):
        '''
        登録画面で選択できる取引先情報を検索する
        '''
        companyJson = json.dumps(
            list(Company.objects
                 .filter(belong_user=self.request.user.email)
                 .values('company_name')
                 .order_by('company_name')
                 )
        )
        return companyJson

    def registCompany(self, companyName):
        '''
        会社名の存在有無を確認し、存在しなければ登録する
        '''
        exist = (Company.objects
                 .filter(
                     belong_user=self.request.user.email,
                     company_name=companyName,
                 ).exists()
                 )

        if not exist:
            company = Company()
            company.belong_user = self.request.user.email
            company.company_name = companyName
            company.regist_user = self.request.user.email
            # company.regist_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            company.regist_date = self.request.requestDateTime
            company.save()

    def registSuitou(self, form, detailFormset):
        '''
        商品情報を登録する
        '''
        # 保存対象の出納オブジェクトを取得する（この時点ではコミットしない）
        suitou = form.save(commit=False)

        # 画面からPOSTされたデータの他に必須のデータをセットして保存する
        suitou.belong_user = self.request.user.email
        suitou.total_price = 0  # TODO:このカラムは使用しないため削除する
        suitou.regist_user = self.request.user.email
        # suitou.regist_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        suitou.regist_date = self.request.requestDateTime
        suitou.save()

        for detail in detailFormset.save(commit=False):
            detail.belong_user = self.request.user.email
            detail.regist_user = self.request.user.email
            # detail.regist_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            detail.regist_date = self.request.requestDateTime
            detail.suitou = suitou
        detailFormset.save()

    def updateSuitou(self, form, formset):
        '''
        出納情報を更新する
        '''
        suitou = form.save(commit=False)
        detailList = formset.save(commit=False)

        # 画面からPOSTされたデータの他に必要なデータをセットして保存する
        suitou.total_price = 0  # TODO:このカラムは使用しないため削除する
        suitou.update_user = self.request.user.email
        # suitou.update_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        suitou.update_date = self.request.requestDateTime
        suitou.save()

        for detail in detailList:
            if detail.id is None:
                # 新規追加レコードの場合
                detail.belong_user = self.request.user.email
                detail.regist_user = self.request.user.email
                # detail.regist_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                detail.regist_date = self.request.requestDateTime
                detail.suitou = suitou
            else:
                # 更新レコードの場合
                detail.update_user = self.request.user.email
                # detail.update_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                detail.update_date = self.request.requestDateTime

        formset.save()
