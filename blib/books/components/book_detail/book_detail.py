from django_components import Component
from django_components import register


@register("book_detail")
class BookDetails(Component):
    template_name = "book_detail.html"

    class Media:
        css = "book_detail.css"
        js = "book_detail.js"
