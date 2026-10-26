
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial Django admin account"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            raise CommandError(
                "Set all DJANGO_SUPERUSER environment variables."
            )

        User = get_user_model()

        if User.objects.filter(**{User.USERNAME_FIELD: username}).exists():
            raise CommandError(
                "This username or login identifier already exists. "
                "No account was changed."
            )

        user = User.objects.create_superuser(
            **{
                User.USERNAME_FIELD: username,
                "email": email,
                "password": password,
            }
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser {user} created successfully."
            )
        )
