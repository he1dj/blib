import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Subscriptions, Tag, Category

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(email='testuser@example.com', password='password')

@pytest.fixture
def tag(db):
    return Tag.objects.create(title='Test Tag')

@pytest.fixture
def category(db):
    return Category.objects.create(title='Test Category')

@pytest.fixture
def subscription(user, tag, category):
    subscription = Subscriptions.objects.create(user=user)
    subscription.tags.add(tag)
    subscription.categories.add(category)
    return subscription

# Test case for creating a new subscription
def test_create_subscription(api_client, user, tag, category):
    api_client.login(email='testuser@example.com', password='password')
    data = {
        'tags': [tag.id],
        'categories': [category.id],
        'subscribed_users': []
    }
    response = api_client.post('/subscriptions/', data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Subscriptions.objects.count() == 1
    assert Subscriptions.objects.get().user == user

# Test case for updating an existing subscription
def test_update_subscription(api_client, subscription, tag):
    api_client.login(email='testuser@example.com', password='password')
    new_tag = Tag.objects.create(title='New Tag')
    data = {
        'tags': [tag.id, new_tag.id],
        'categories': [],
        'subscribed_users': []
    }
    response = api_client.put(f'/subscriptions/{subscription.id}/', data)
    assert response.status_code == status.HTTP_200_OK
    subscription.refresh_from_db()
    assert set(subscription.tags.all()) == {tag, new_tag}

# Test case for unique subscription per user
def test_unique_subscription_per_user(api_client, user, tag, category):
    api_client.login(email='testuser@example.com', password='password')
    data = {
        'tags': [tag.id],
        'categories': [category.id],
        'subscribed_users': []
    }
    # Create the first subscription
    response = api_client.post('/subscriptions/', data)
    assert response.status_code == status.HTTP_201_CREATED

    # Try creating a second subscription for the same user
    response = api_client.post('/subscriptions/', data)
    assert response.status_code == status.HTTP_200_OK  # Should update instead of creating a new one
    assert Subscriptions.objects.count() == 1

# Test case for getting subscriptions
def test_get_subscriptions(api_client, subscription):
    api_client.login(email='testuser@example.com', password='password')
    response = api_client.get('/subscriptions/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['user'] == subscription.user.id
    