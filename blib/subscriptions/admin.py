from django.contrib import admin
from .models import Subscriptions


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('tags', 'categories', 'subscribed_users',)

admin.site.register(Subscriptions, SubscriptionAdmin)
