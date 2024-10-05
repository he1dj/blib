from .models import Subscriptions, Tag, Category
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SubscriptionsSerializer(serializers.ModelSerializer):
    
    """
    We use PrimaryKeyRelatedField, which allows us to work with object IDs. 
    The API expects you to pass only IDs of existing tags, categories, and users.

    """
    
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    subscribed_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    
    class Meta:
        model = Subscriptions
        fields = ("tags", "categories", "subscribed_users")
        
    def create(self, validated_data):
        # Get the current user
        user = self.context['request'].user
        
        # Create a subscription for the current user  
        subscription, created = Subscriptions.objects.get_or_create(user=user)
    
        # Set the tags, categories, and subscribed_users for the subscription
        subscription.tags.set(validated_data['tags'])
        subscription.categories.set(validated_data['categories'])
        subscription.subscribed_users.set(validated_data['subscribed_users'])
        
        subscription.save()
        return subscription