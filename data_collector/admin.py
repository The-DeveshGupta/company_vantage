from django.contrib import admin
from .models import Ticker, StocksPrice


class ShowDateInAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Ticker, ShowDateInAdmin)
admin.site.register(StocksPrice, ShowDateInAdmin)
