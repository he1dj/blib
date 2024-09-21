from django.utils.text import slugify
from wagtail.admin.forms import WagtailAdminPageForm


class BookForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if not cleaned_data.get("slug"):
            cleaned_data["slug"] = slugify(title)
        return cleaned_data
