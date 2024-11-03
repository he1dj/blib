
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from blib.user_profiles.models import UserProfile


class User(AbstractUser):
    """
    Custom user model for the application `blib`. This model extends the default Django `AbstractUser`
    by replacing `email` as the primary identifier and adding an optional `profile` field for linking
    a `UserProfile` instance.

    Fields:
        name (str): Optional first name of the user.
        last_name (str): Optional last name of the user.
        email (str): Primary identifier for login, must be unique.
        username (str): Optional unique nickname. Auto-generated if left blank during creation.
        profile (OneToOneField): Links to a `UserProfile` instance. Created automatically when a user is saved.

    Attributes:
        USERNAME_FIELD (str): Designates `email` as the unique identifier for user login.
        REQUIRED_FIELDS (list): Required fields for user creation. Empty here since we only use `email`.

    Methods:
        get_absolute_url (str): Returns the URL for the user's profile view.
        generate_username (str): Generates a unique username based on email if not provided.

    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("Username (Nickname)"), blank=True,max_length=255, unique=True)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def save(self, *args, **kwargs):
        """
        Overridden save method to generate a unique username if not provided.
        """
        self.generate_username()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """
        Returns the URL for the user's detail view.

        Returns:
            str: URL path to access the detail page of the user.
        """
        return reverse("user_profile:detail", kwargs={"pk": self.id})

    def generate_username(self):
        """
        Generates a unique username based on the email if `username` field is empty.

        This function splits the email at `@`, uses the prefix as a base, and appends a number
        if a user with the same username already exists.

        Returns:
            str: The generated unique username.

        Raises:
            IntegrityError: If the unique constraint fails during save operation.
        """

        if not self.username:
            base_username = self.email.split('@')[0]
            potential_username = base_username
            counter = 1

            # We save within the transaction, minimizing the risk of duplicates.
            with transaction.atomic():
                while User.objects.filter(username=potential_username).exists():
                    potential_username = f"{base_username}{counter}"
                    counter += 1

                self.username = potential_username
                self.save()
        return self.username

    def __str__(self) -> str:
        """
        Returns a string representation of the user.

        Returns:
            str: String representation of the user.
        """
        return self.username
