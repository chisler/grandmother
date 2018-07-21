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

    def __str__(self):
        return self.name


# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()