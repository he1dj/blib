from django.db import models
from blib.books.models import Tag, Category
from django.conf import settings


class Subscriptions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    tags = models.ManyToManyField(Tag, related_name='subscribed_tags')
    categories = models.ManyToManyField(Category, related_name='subscribed_categories')
    subscribed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscribed_users')
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.user.username} subscriptions" 