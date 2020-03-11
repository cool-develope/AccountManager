from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from . import views

urlpatterns = [
    url(r'^record_history/(?P<account_id>\d+)/$', login_required(views.RecordHistoryView.as_view()), name = 'record_history'),
    url(r'^account_list/(?P<trade_type>\w+)/$', login_required(views.AccountListView.as_view()), name = 'account_list'),
    url(r'^account_history/(?P<account_id>\d+)/$', login_required(views.AccountHistoryView.as_view()), name = 'account_history'),
    url(r'^account_history/(?P<trade_type>\w+)/$', login_required(views.AccountHistoryView.as_view()), name = 'account_histories'),
    url(r'^rebalance_list/$', login_required(views.RebalanceListView.as_view()), name = 'rebalance_list'),
    url(r'^rebalance_history/(?P<pair_id>\d+)/$', login_required(views.RebalanceHistoryView.as_view()), name = 'rebalance_history'),
    url(r'^rebalance_history/$', login_required(views.RebalanceHistoryView.as_view()), name = 'rebalance_histories'),
]