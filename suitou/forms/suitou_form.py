from django import forms
from django.forms import modelformset_factory
from app_table.models import Suitou
from app_table.models import SuitouDetail


class SuitouForm(forms.ModelForm):
    '''
    納品フォーム
    '''
    class Meta:
        model = Suitou
        fields = {'suitou_date', 'suitousaki', 'memo'}
        widgets = {
            'suitou_date': forms.DateInput(
                attrs={
                    'id': 'regist_suitou_date',
                    'type': 'date',
                    'style': 'width: 17rem;',
                    'class': 'form-control form-control-lg',
                }
            ),
            'suitousaki': forms.TextInput(
                attrs={
                    # 'id': 'regist_suitousaki',
                    'type': 'search',
                    'list': 'company_list',
                    'class': 'form-control form-control-lg',
                }
            ),
            'memo': forms.Textarea(
                attrs={
                    'id': 'regist_memo',
                    'rows': '3',
                    'class': 'form-control form-control-lg',
                }
            ),
        }


class SuitouDetailForm(forms.ModelForm):
    '''
    納品詳細フォーム
    '''
    class Meta:
        model = SuitouDetail
        fields = {'kataban', 'price', 'amount'}
        widgets = {
            'kataban': forms.TextInput(
                attrs={
                    'type': 'search',
                    'list': 'shohin_list',
                    'class': 'form-control form-control-lg js_shohin',
                }
            ),
            'price': forms.TextInput(
                attrs={
                    'type': 'number',
                    'min': '0',
                    'class': 'form-control form-control-lg js_price',
                }
            ),
            'amount': forms.TextInput(
                attrs={
                    'type': 'number',
                    'min': '0',
                    'class': 'form-control form-control-lg js_amount',
                }
            ),
        }


SuitouDetailFormset = modelformset_factory(
    SuitouDetail,
    form=SuitouDetailForm,
    extra=5,
    max_num=5,
    can_delete=True,
)
