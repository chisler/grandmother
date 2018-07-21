from django.contrib import admin

from subscription.models import Subscription, CurrencyBalance, DateBalance


class CurrencyBalanceInline(admin.TabularInline):
    model = CurrencyBalance
    # raw_id_fields = ("name",)


class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [
        CurrencyBalanceInline,
    ]


admin.site.register(Subscription, SubscriptionAdmin)
