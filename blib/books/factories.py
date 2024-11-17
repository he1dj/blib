import random
import secrets
import shutil
from pathlib import Path

import factory
from django.conf import settings
from django.core.files import File
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from faker import Faker

from blib.books.models import Author
from blib.books.models import Book
from blib.books.models import BookAuthorRelationship
from blib.books.models import BookCategoryRelationship
from blib.books.models import BookTagRelationship
from blib.books.models import Category
from blib.books.models import Tag

fake = Faker()


def generate_unique_slug(model_class, title):
    """Generate a unique slug for a model."""
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: generate_unique_slug(Category, obj.title))


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: generate_unique_slug(Tag, obj.title))


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    middle_name = factory.Faker("first_name", locale="en_US")


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=3)
    slug = factory.LazyAttribute(lambda obj: generate_unique_slug(Book, obj.title))
    published_date = factory.Faker("date_between", start_date="-10y", end_date="today")
    number_of_pages = factory.Faker("random_int", min=50, max=1000)
    description = factory.Faker("paragraph")
    pdf = factory.LazyAttribute(lambda _: clone_pdf("mock.pdf"))
    # cover_image = factory.django.ImageField(
    #     filename="mock/mock_cover.jpg",
    #     width=200,
    #     height=300,
    # )
    file_size = "500 KB"

    @factory.post_generation
    def add_authors(self, create, extracted, **kwargs):
        if not create:
            return
        num_authors = secrets.randbelow(3) + 1
        if extracted:
            authors = random.sample(extracted, min(len(extracted), num_authors))
        else:
            authors = AuthorFactory.create_batch(num_authors)
        for author in authors:
            BookAuthorRelationship.objects.create(Book=self, author=author)

    @factory.post_generation
    def add_categories(self, create, extracted, **kwargs):
        if not create:
            return
        num_categories = secrets.randbelow(2) + 1
        if extracted:
            categories = random.sample(extracted, min(len(extracted), num_categories))
        else:
            categories = CategoryFactory.create_batch(num_categories)
        for category in categories:
            BookCategoryRelationship.objects.create(Book=self, category=category)

    @factory.post_generation
    def add_tags(self, create, extracted, **kwargs):
        if not create:
            return
        num_tags = secrets.randbelow(4) + 1
        if extracted:
            tags = random.sample(extracted, min(len(extracted), num_tags))
        else:
            tags = TagFactory.create_batch(num_tags)
        for tag in tags:
            BookTagRelationship.objects.create(Book=self, tag=tag)


def clone_pdf(source_file):
    source_path = Path(source_file)
    media_path = Path(settings.MEDIA_ROOT) / source_path.name
    destination_dir = Path(settings.MEDIA_ROOT) / "books" / "pdfs"
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{source_path.stem}_copy{source_path.suffix}"
    if not media_path.exists():
        msg = f"Source file '{media_path}' does not exist."
        raise FileNotFoundError(msg)
    shutil.copy(media_path, destination)
    return File(destination.open("rb"), name=destination.name)
