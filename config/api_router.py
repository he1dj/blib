from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from blib.users.api.views import UserViewSet
from blib.subscriptions.views import SubscriptionsViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("subscriptions", SubscriptionsViewSet)

app_name = "api"
urlpatterns = router.urls
