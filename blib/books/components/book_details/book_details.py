from django_components import Component
from django_components import register


@register("book_details")
class BookDetails(Component):
    template_name = "book_details.html"

    # def get_context_data(self, book):
    #     return {
    #         "book": book,
    #     }

    class Media:
        css = "book_details.css"
        js = "book_details.js"
