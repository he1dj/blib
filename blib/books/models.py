import io
from pathlib import Path

import PyPDF2
import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.models import ClusterableModel
from wagtail.models import ParentalKey
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=55, blank=False)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


@register_snippet
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=55, blank=False)

    class Meta:
        verbose_name_plural = "tags"

    def __str__(self):
        return self.title


@register_snippet
class Author(index.Indexed, ClusterableModel):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    middle_name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "authors"

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name}"


@register_snippet
class Book(index.Indexed, ClusterableModel):
    id = models.AutoField(primary_key=True)
    uuid = ShortUUIDField(unique=True, length=8, max_length=10)
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True, max_length=55, blank=False)
    published_date = models.DateField(blank=False)
    number_of_pages = models.IntegerField(blank=False, default=0)
    description = models.TextField(max_length=1024, blank=True)
    pdf = models.FileField(upload_to="books/pdfs/")
    cover_image = models.ImageField(upload_to="books/covers/", blank=True)
    public_url = models.URLField(blank=True, null=False, default="")
    qr_code = models.ImageField(upload_to="books/qr_codes/", blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    file_size = models.CharField(max_length=50, blank=True)
    panels = [
        FieldPanel("uuid", read_only=True),
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("book_author_relationship", label="Authors"),
        FieldPanel("published_date"),
        FieldPanel("number_of_pages"),
        FieldPanel("description"),
        InlinePanel("book_category_relationship", label="Categories"),
        InlinePanel("book_tag_relationship", label="Tags"),
        FieldPanel("pdf"),
        FieldPanel("cover_image"),
        FieldPanel("public_url", read_only=True),
        FieldPanel("qr_code", read_only=True),
        FieldPanel("upload_date", read_only=True),
        FieldPanel("last_edited", read_only=True),
        FieldPanel("file_size", read_only=True),
    ]
    search_fields = [
        index.SearchField("title"),
        index.AutocompleteField("title"),
        index.FilterField("published_date"),
        index.FilterField("number_of_pages"),
        index.FilterField("file_size"),
        index.RelatedFields(
            "book_category_relationship",
            [
                index.FilterField("category__title"),
            ],
        ),
        index.RelatedFields(
            "book_tag_relationship",
            [
                index.FilterField("tag__title"),
            ],
        ),
    ]

    class Meta:
        verbose_name_plural = "books"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        self.public_url = self.generate_public_url()
        self.qr_code = self.generate_qr_code(self.public_url)
        self.number_of_pages = self.get_book_pages()
        self.file_size = self.get_file_size()
        super().save(*args, **kwargs)

    def generate_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Book.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def get_book_pages(self):
        pdf_path = Path(self.pdf.path)
        with pdf_path.open("rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)

    def get_file_size(self):
        pdf_path = Path(self.pdf.path)
        file_size_bytes = pdf_path.stat().st_size
        mb = 1024
        if file_size_bytes < mb:
            return f"{file_size_bytes} bytes"
        if file_size_bytes < mb ** 2:
            return f"{file_size_bytes / mb:.2f} KB"
        return f"{file_size_bytes / (mb ** 2):.2f} MB"

    def generate_public_url(self):
        site_url = settings.SITE_URL
        return f"{site_url}/books/{self.uuid}/{self.slug}"

    def generate_qr_code(self, url):
        qr = qrcode.make(url)
        qr_file = io.BytesIO()
        qr.save(qr_file, "PNG")
        qr_file.seek(0)
        return ContentFile(qr_file.read(), name=f"qr_{self.uuid}_{self.slug}.png")

    @property
    def authors(self):
        return [n.author for n in self.book_author_relationship.all()]

    @property
    def categories(self):
        return [n.category for n in self.book_category_relationship.all()]

    @property
    def tags(self):
        return [n.tag for n in self.book_tag_relationship.all()]


class BookAuthorRelationship(index.Indexed, models.Model):
    id = models.AutoField(primary_key=True)
    Book = ParentalKey("Book", related_name="book_author_relationship")
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="+")
    panels = [FieldPanel("author")]
    index.RelatedFields(
        "book",
        [
            index.SearchField("title"),
            index.FilterField("published_date"),
            index.FilterField("number_of_pages"),
        ],
    )

    def __str__(self) -> str:
        return super().__str__()


class BookCategoryRelationship(index.Indexed, models.Model):
    id = models.AutoField(primary_key=True)
    Book = ParentalKey("Book", related_name="book_category_relationship")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="+")
    panels = [FieldPanel("category")]
    index.RelatedFields(
        "book",
        [
            index.SearchField("title"),
            index.FilterField("published_date"),
            index.FilterField("number_of_pages"),
        ],
    )

    def __str__(self) -> str:
        return super().__str__()


class BookTagRelationship(index.Indexed, models.Model):
    id = models.AutoField(primary_key=True)
    Book = ParentalKey("Book", related_name="book_tag_relationship")
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="+")
    panels = [FieldPanel("tag")]
    index.RelatedFields(
        "book",
        [
            index.SearchField("title"),
            index.FilterField("published_date"),
            index.FilterField("number_of_pages"),
        ],
    )

    def __str__(self) -> str:
        return super().__str__()
