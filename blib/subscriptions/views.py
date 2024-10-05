from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from.models import Subscriptions
from.serializers import SubscriptionsSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        # Filter only subscriptions for the current user
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Create a subscription for the current user
        return serializer.save(user=self.request.user)
    