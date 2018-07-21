from users.models import User, get_total_for_currency_balances
from django.db import models


class Subscription(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed_by')
    money_allocated = models.FloatField()
    initial_ratio = models.FloatField()

    class Meta:
        unique_together = ('follower', 'user_followed', )

    def __str__(self):
        return f'{self.follower} is following {self.user_followed}'

    def get_total_money(self):
        from subscription.models import CurrencyBalance

        currency_balances = CurrencyBalance.objects.filter(subscription=self)
        return get_total_for_currency_balances(currency_balances)


class CurrencyBalance(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    amount = models.FloatField()

    class Meta:
        unique_together = ('name', 'subscription')


class DateBalance(models.Model):
    user = models.ForeignKey(User, related_name='date_balances', on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    date = models.DateField()