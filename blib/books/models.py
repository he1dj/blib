import io

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Book(models.Model):
    uuid = ShortUUIDField(unique=True, length=8, max_length=10)
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True, max_length=55, blank=False)
    author = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, blank=True)
    pdf = models.FileField(upload_to="books/pdfs/")
    cover_image = models.ImageField(upload_to="books/covers/", blank=True)
    public_url = models.URLField(blank=True, null=False, default="")
    qr_code = models.ImageField(upload_to="books/qr_codes/", blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("uuid", read_only=True),
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("author"),
        FieldPanel("description"),
        FieldPanel("pdf"),
        FieldPanel("cover_image"),
        FieldPanel("public_url", read_only=True),
        FieldPanel("qr_code", read_only=True),
        FieldPanel("upload_date", read_only=True),
    ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        self.public_url = self.generate_public_url()
        self.qr_code = self.generate_qr_code(
            self.public_url,
        )
        super().save(*args, **kwargs)

    def generate_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Book.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def generate_public_url(self):
        site_url = settings.SITE_URL
        return f"{site_url}/books/{self.uuid}/{self.slug}"

    def generate_qr_code(self, url):
        qr = qrcode.make(url)
        qr_file = io.BytesIO()
        qr.save(qr_file, "PNG")
        qr_file.seek(0)
        return ContentFile(qr_file.read(), name=f"qr_{self.uuid}_{self.slug}.png")
