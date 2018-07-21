from collections import defaultdict

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

    def __str__(self):
        return f'User {self.id}'

    def get_total_money(self):
        from subscription.models import CurrencyBalance

        currency_balances = CurrencyBalance.objects.filter(subscription__follower=self)
        return get_total_for_currency_balances(currency_balances)
