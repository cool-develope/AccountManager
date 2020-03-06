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

class Account(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="accounts")

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

class Rebalance(models.Model):
    from_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name="from_rebalances")
    to_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name="to_rebalances")
    
    request_date = models.DateTimeField(auto_now_add = False, blank = True, default = timezone.now)
    enter_date = models.DateTimeField(auto_now_add = False, blank = True, default = timezone.now)
    finish_date = models.DateTimeField(auto_now_add = False, blank = True, default = timezone.now)

    amount = models.DecimalField(max_digits = 20, decimal_places = 2, blank = True, default = 0)
    
    urgency = models.ForeignKey('Urgency', on_delete=models.CASCADE, related_name="rebalances")

    period = models.CharField(max_length=100)
    reason = models.TextField(blank=True)

    STATE_CHOICES = [
        ('RQ', 'Request'),
        ('PR', 'Processing'),
        ('FS', 'Finish'),
    ]

    state = models.CharField(max_length=10, choices=STATE_CHOICES)

