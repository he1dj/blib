from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.admin.panels import MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from wagtail.models import Page
from wagtail.search import index


class BlogPage(Page):
    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    search_fields = [*Page.search_fields, index.SearchField("body"), index.FilterField("date")]
    content_panels = [*Page.content_panels, FieldPanel("date"), FieldPanel("body"), InlinePanel("related_links", heading="Related links", label="Related link")]
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel("feed_image"),
    ]
    parent_page_types = ["blog.BlogIndex"]
    subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="related_links")
    name = models.CharField(max_length=255)
    url = models.URLField()
    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = [*Page.content_panels, FieldPanel("body")]
