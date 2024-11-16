from django_components import Component
from django_components import register


@register("search_dropdown")
class SearchDropdown(Component):
    template_name = "search_dropdown.html"

    class Media:
        css = "search_dropdown.css"
        js = "search_dropdown.js"
