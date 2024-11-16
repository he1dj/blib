from django.core.management.base import BaseCommand

from blib.books.factories import AuthorFactory
from blib.books.factories import BookFactory
from blib.books.factories import CategoryFactory
from blib.books.factories import TagFactory


class Command(BaseCommand):
    help = "Populate the database with mock data"

    def handle(self, *args, **kwargs):
        # Create Categories
        self.stdout.write("Creating categories...")
        categories = CategoryFactory.create_batch(10)

        # Create Tags
        self.stdout.write("Creating tags...")
        tags = TagFactory.create_batch(20)

        # Create Authors
        self.stdout.write("Creating authors...")
        authors = AuthorFactory.create_batch(15)

        # Create Books
        self.stdout.write("Creating books...")
        for _ in range(30):
            BookFactory(add_authors=authors, add_categories=categories, add_tags=tags)

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
