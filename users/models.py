from collections import defaultdict

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        return f'User {self.id}'

    def get_total_money(self):
        from subscription.models import CurrencyBalance

        currency_balances = CurrencyBalance.objects.filter(subscription__follower=self)

        currency_dict = defaultdict(float)
        for c in currency_balances:
            currency_dict[c.name] += c.amount

