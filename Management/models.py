from django.db import models
from django.utils import timezone

# Create your models here.

class Currency(models.Model):
    name = models.CharField(max_length=100)
    display = models.CharField(max_length=100)

    def __str__(self):
        return self.display

class Urgency(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length = 100)
    comment = models.TextField(blank = True)

    host = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="accounts")

    client = models.ForeignKey('Client', on_delete = models.CASCADE, related_name = 'accounts')

    balance = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    margin = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    free_margin = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    equity = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    swap_profit = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    profit = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    open_lots = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)

    def __str__(self):
        return self.tag

class History(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name="histories")
    open_date = models.DateTimeField(auto_now_add = False, blank = True, default = timezone.now)

    amount = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)

    PROCESS_CHOICES = [
        ('W', 'Withdraw'),
        ('D', 'Deposit'),
    ]

    process_type = models.CharField(max_length=10, choices=PROCESS_CHOICES)

    class Meta:
        ordering = ('-open_date', )

class AccountPairs(models.Model):
    name = models.CharField(max_length=100)
    first_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name="from_pair")
    second_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name="to_pair")
    
    comment = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Rebalance(models.Model):
    pair = models.ForeignKey('AccountPairs', on_delete=models.CASCADE, related_name="rebalances")
    direct = models.BooleanField(default=True)

    request_date = models.DateTimeField(auto_now_add = False, blank = True, default = timezone.now)
    enter_date = models.DateTimeField(auto_now_add = False, blank = True, default = timezone.now)
    finish_date = models.DateTimeField(auto_now_add = False, blank = True, default = timezone.now)

    amount = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    
    urgency = models.ForeignKey('Urgency', on_delete=models.CASCADE, related_name="rebalances")

    period = models.CharField(max_length=100)
    reason = models.TextField(blank=True)

    STATE_CHOICES = [
        ('WT', 'Wait'),
        ('RQ', 'Request'),
        ('PR', 'Processing'),
        ('FS', 'Finish'),
    ]

    state = models.CharField(max_length=10, choices=STATE_CHOICES)

    class Meta:
        ordering = ('-request_date', )


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from AccountManager import consumers

@receiver(pre_save, sender=Rebalance)
def param_handler(sender, instance, *args, **kwargs):
    if instance.pk:
        prev_state = Rebalance.objects.get(pk = instance.pk).state
        print(prev_state, instance.state)
        if (prev_state == 'WT' and instance.state == 'RQ') or instance.state == 'FS':
            msg = "%s;%d;" % (instance.state, instance.pk)
            if (instance.direct):
                msg += "%s;%s;" % (instance.pair.first_account, instance.pair.second_account)
            else:
                msg += "%s;%s;" % (instance.pair.second_account, instance.pair.first_account)
            msg += instance.request_date.strftime("%B %d, %Y, %I:%M %p") + ";%f %s;%s;%s" % (float(instance.amount), instance.pair.first_account.currency, instance.urgency, instance.period)
            consumers.send_rebalance_report(msg)
            consumers.send_log(msg)