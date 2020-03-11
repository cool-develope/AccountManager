from django.shortcuts import render
from django.views.generic import TemplateView
from Management import models as manage_model
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()

        return context


class AccountListView(TemplateView):
    template_name = "manage/accounts.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['pairs'] = manage_model.AccountPairs.objects.filter(client__trade_type = kwargs['trade_type'])
        context['trade_type'] = kwargs['trade_type']

        return context

class AccountHistoryView(TemplateView):
    template_name = "manage/account_history.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        if 'account_id' in kwargs:
            account = manage_model.Account.objects.get(id = kwargs['account_id'])
            context['histories'] = account.histories.all()[:10]
            context['is_all'] = False
            context['account'] = account
        else:
            context['histories'] = manage_model.History.objects.filter(account__client__trade_type = kwargs['trade_type'])[:10]
            context['trade_type'] = kwargs['trade_type']
            context['is_all'] = True
        return context

class RecordHistoryView(TemplateView):
    template_name = "manage/account_record.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        account = manage_model.Account.objects.get(id = kwargs['account_id'])
        context['records'] = account.records.all()[:25]
        context['account'] = account
        return context

class RebalanceListView(TemplateView):
    template_name = "manage/rebalances.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['rebalances'] = manage_model.Rebalance.objects.filter(Q(state='RQ')|Q(state='PR'))
        return context

    def post(self, request, **kwargs):
        reb_id = request.POST.get("reb_id")
        rebalance = manage_model.Rebalance.objects.get(id = reb_id)
        rebalance.enter_date = timezone.now()
        rebalance.state = "PR"
        rebalance.save()

        return JsonResponse({"status": "ok"})

class RebalanceHistoryView(TemplateView):
    template_name  = "manage/rebalance_history.html"

    def get_context_data(self, **kwargs):
        context  = super(TemplateView, self).get_context_data()
        if 'pair_id' in kwargs:
            pair = manage_model.AccountPairs.objects.get(id = kwargs['pair_id'])
            context['rebalances'] = pair.rebalances.filter(state = 'FS').all()[:10]
            context['is_all'] = False
            context['pair'] = pair
        else:
            context['rebalances'] = manage_model.Rebalance.objects.filter(state = 'FS')[:10]
            context['is_all'] = True
        return context