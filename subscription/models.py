from users.models import User
from django.db import models


class Subscription(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed_by')
    money_allocated = models.FloatField()
    initial_ration = models.FloatField()

    def __str__(self):
        return f'{self.follower} is following {self.user_followed}'


class CurrencyBalance(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    amount = models.FloatField()

    class Meta:
        unique_together = ('name', 'subscription')