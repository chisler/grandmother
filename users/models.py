from collections import defaultdict
from django.db import models

from django.contrib.auth.models import AbstractUser

def get_rates(currency, amount):
    return amount * 10

def get_total_for_currency_balances(currency_balances):
    currency_dict = defaultdict(float)
    for c in currency_balances:
        currency_dict[c.name] += c.amount

    total = 0
    for currency, amount in currency_dict.items():
        total += get_rates(currency, amount)
    return total

class User(AbstractUser):
    TRADER = 1
    INVESTOR = 2
    ROLE_CHOICES = (
        (TRADER, 'Trader'),
        (INVESTOR, 'Investor'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    api_key = models.CharField(max_length=500, default='')
    secret_key = models.CharField(max_length=500, default='')
    initial_money = models.FloatField(default=0)
    free_money = models.FloatField(default=0)

    def __str__(self):
        return f'User {self.id} {self.username}'

    def get_total_money(self):
        from subscription.models import CurrencyBalance

        currency_balances = CurrencyBalance.objects.filter(subscription__follower=self)
        return get_total_for_currency_balances(currency_balances)
