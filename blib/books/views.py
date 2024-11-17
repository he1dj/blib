from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import ListView

from blib.books.components.book_list.book_list import BookListComponent
from blib.books.models import Book


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if self.request.htmx:
            html = BookListComponent.render(context)
            return HttpResponse(html)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        sort_by = self.request.GET.get("sort", "upload_date")
        direction = self.request.GET.get("direction", "desc")

        if sort_by not in ["upload_date", "title"]:
            sort_by = "upload_date"
        if direction not in ["asc", "desc"]:
            direction = "desc"

        queryset = Book.objects.all().prefetch_related(
            "book_author_relationship__author",
            "book_category_relationship__category",
            "book_tag_relationship__tag",
        )
        if direction == "asc":
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by(f"-{sort_by}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get("sort", "upload_date")
        direction = self.request.GET.get("direction", "desc")
        context["sort_by"] = sort_by
        context["direction"] = direction
        return context


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, uuid=self.kwargs["uuid"])
        slug = self.kwargs.get("slug")
        if not slug or book.slug != slug:
            return redirect("books:book_details", uuid=book.uuid, slug=book.slug)
        self.object = book
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
