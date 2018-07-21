from django.contrib import admin

from subscription.models import DateBalance
from users.models import User


class DateBalanceAdmin(admin.TabularInline):
    model = DateBalance


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'role']
    inlines = [DateBalanceAdmin]

admin.site.register(User, UserAdmin)