from django.views.generic import ListView
from wagtail.search.backends import get_search_backend
from wagtail.search.utils import parse_query_string

from blib.books.models import Author
from blib.books.models import Book
from blib.books.models import Category
from blib.books.models import Tag


class SearchView(ListView):
    template_name = "search/search.html"
    context_object_name = "search_results"
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all()
        s = get_search_backend()
        query = self.request.GET.get("q", "")
        query_parts = [query] if query else []
        year_filter = self.request.GET.get("year")
        authors_filter = self.request.GET.get("authors")
        category_filter = self.request.GET.get("categories")
        tag_filter = self.request.GET.get("tags")
        if year_filter:
            query_parts.append(f"year:{year_filter}")
        if authors_filter:
            query_parts.append(f"authors:{authors_filter}")
        if category_filter:
            query_parts.append(f"categories:{category_filter}")
        if tag_filter:
            query_parts.append(f"tags:{tag_filter}")
        query_string = " ".join(query_parts).strip()
        filters, query = parse_query_string(query_string, operator="and")
        year_filter = filters.get("year")
        authors_filter = filters.get("author")
        category_filter = filters.get("category")
        tag_filter = filters.get("tag")
        if year_filter:
            queryset = queryset.filter(published_date__year=year_filter)
        if authors_filter:
            queryset = queryset.filter(
                book_author_relationship__author__name__iexact=authors_filter,
            )
        if category_filter:
            queryset = queryset.filter(
                book_category_relationship__category__name__iexact=category_filter,
            )
        if tag_filter:
            queryset = queryset.filter(
                book_tag_relationship__tag__name__iexact=tag_filter,
            )
        return s.search(query, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["years"] = Book.objects.dates("published_date", "year", order="DESC")
        context["authors"] = Author.objects.all()
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        return context
