from background_task import background
from Management import models as manage_model
from background_task.models import Task
from . import consumers
import pika
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

@background(schedule=1)
def bind_message(client_name):
    client = manage_model.Client.objects.get(name = client_name)
    print("while binding", client.name)
    host = client.host
    prefix = client.name

    credentials = pika.PlainCredentials('client', 'client')
    flag = False
    try:
    # if True:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host,
                                    5672,
                                    '/',
                                    credentials)
        )

        channel = connection.channel()
        flag = True
        ex_name = prefix + "_Upload"
        channel.exchange_declare(exchange = ex_name, exchange_type="direct", durable = True)
        queue_name = prefix + "_Account"
        channel.queue_declare(queue = queue_name)
        channel.queue_bind(exchange = ex_name, routing_key = "route", queue = queue_name)
        channel.basic_consume(queue = queue_name, on_message_callback = callback, auto_ack = True)
    
        channel.start_consuming()
    except Exception as e:
        print_error(e)
    finally:
        if flag:
            channel.stop_consuming()
            connection.close()
        return

def callback(channel, method, properties, body):
    exchange = method.exchange
    client_name, _ = exchange.split('_')
    client = manage_model.Client.objects.get(name = client_name)
    routing_key = method.routing_key
    body = body.decode('utf-8')
    header, message = body.split('>>')
    if header == "AccountReport":
        account_report_analyse(client, message)
    if header == "Rebalance":
        rebalance_report_analyse(client, message)

def rebalance_report_analyse(client, message):
    str_list = message.split(';')
    is_direct = True
    try:
        first_account = manage_model.Account.objects.get(client = client, name = str_list[1])
        second_account = manage_model.Account.objects.get(client = client, name = str_list[2])
    
        amount = float(str_list[3])

        if manage_model.AccountPairs.objects.filter(first_account = first_account, second_account = second_account).exists():
            pair = manage_model.AccountPairs.objects.get(first_account = first_account, second_account = second_account)
        else:
            is_direct = False
            pair = manage_model.AccountPairs.objects.get(first_account = second_account, second_account = first_account)

    except ObjectDoesNotExist:
        return
    manage_model.Rebalance.objects.create(pair = pair, direct = is_direct, amount = amount, urgency = manage_model.Urgency.objects.get(name = "Regular"), period = "3 days", state = "WT")

def account_report_analyse(client, message):
    str_list = message.split(';')
    
    balance = float(str_list[1])
    margin = float(str_list[2])
    profit = float(str_list[3])
    swap_profit = float(str_list[4])
    open_lots = float(str_list[5])
    is_base = (str_list[6] == "True")
    equity = balance + profit + swap_profit
    
    if str_list[7] == 'daily':
        try:
            account = manage_model.Account.objects.get(client = client, name = str_list[0])
        except ObjectDoesNotExist:
            return
        manage_model.Record.objects.create(account = account, open_date = timezone.now(), balance = balance, equity = equity, open_lots = open_lots)
        return 
    if not is_base:
        return

    try:
        account = manage_model.Account.objects.get(client = client, name = str_list[0])
    except ObjectDoesNotExist:
        return

    account.balance = balance
    account.margin = margin
    account.free_margin = equity - margin
    account.equity = equity
    account.profit = profit
    account.swap_profit = swap_profit
    account.open_lots = open_lots
    account.save()
        
    consumers.send_account_report(account)

def print_error(e):
    print("---------------Start-------------------") 
    print(type(e))
    print(e.args)
    print(e)
    print("----------------End--------------------")

def task_run():
    Task.objects.all().delete()    
    for client in manage_model.Client.objects.all():
        bind_message(client.name, repeat = 5)