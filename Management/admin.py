from django.contrib import admin
from . import models
# Register your models here.

class PairAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_account','second_account')
    search_fields = ('first_account__tag', 'second_account__tag')
    list_filter = ('first_account__tag', 'second_account__tag')
admin.site.register(models.AccountPairs, PairAdmin)

class RebalanceAdmin(admin.ModelAdmin):
    list_display = ('pair', 'request_date', 'amount', 'urgency', 'state')
    search_fields = ('pair__name', 'reason')
    list_filter = ('pair__name', 'urgency', 'state')
admin.site.register(models.Rebalance, RebalanceAdmin)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag', 'client', 'balance', 'free_margin', 'open_lots')
    search_fields = ('name', 'tag', 'client')
    list_filter = ('client__name', 'currency')
admin.site.register(models.Account, AccountAdmin)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'open_date', 'amount', 'process_type')
    search_fields = ('account__tag', 'process_type')
    list_filter = ('account__tag', 'process_type')
admin.site.register(models.History, HistoryAdmin)

admin.site.register(models.Client)
admin.site.register(models.Urgency)
admin.site.register(models.Currency)
