from django.contrib import admin
from .models import Shohin
from .models import Company
from .models import Nohin
from .models import NohinDetail
from .models import Suitou
from .models import SuitouDetail

# Register your models here.
admin.site.register(Shohin)
admin.site.register(Company)


class NohinDetailInline(admin.StackedInline):
    model = NohinDetail
    extra = 3


class NohinAdmin(admin.ModelAdmin):
    inlines = [NohinDetailInline]


class SuitouDetailInline(admin.StackedInline):
    model = SuitouDetail
    extra = 3


class SuitouAdmin(admin.ModelAdmin):
    inlines = [SuitouDetailInline]


admin.site.register(Nohin, NohinAdmin)
admin.site.register(NohinDetail)
admin.site.register(Suitou, SuitouAdmin)
admin.site.register(SuitouDetail)
