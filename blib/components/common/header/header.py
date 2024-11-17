from django_components import Component
from django_components import register


@register("header")
class Header(Component):
    template_name = "header.html"

    class Media:
        css = "header.css"
        js = "header.js"
