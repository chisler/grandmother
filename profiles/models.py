from users.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    TRADER = 1
    INVESTOR = 2
    ROLE_CHOICES = (
        (TRADER, 'Trader'),
        (INVESTOR, 'Investor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    api_key = models.CharField(max_length=500, default='')
    secret_key = models.CharField(max_length=500, default='')
    initial_money = models.FloatField(default=0)
    free_money = models.FloatField(default=0)

    def __str__(self):
        return self.name

