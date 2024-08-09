from django.shortcuts import render
from .models import Book, Author, Review
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator

# Create your views here.


def home(req):
    author = Author.objects.all()
    book = Book.objects.all()
    paginator1 = Paginator(author, 15)
    paginator2 = Paginator(book, 10)
    page1 = req.GET.get('page1')
    page2 = req.GET.get('page2')
    authors = paginator1.get_page(page1)
    books = paginator2.get_page(page2)
    return render(req, 'index.html', {'authors': authors, 'book': books})


class DetailBook(DetailView):
    model = Book
    template_name = 'detail_book.html'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        book = self.get_object()
        rew = Review.objects.filter(book=book)
        print(len(rew))
        all_rew = len(rew)
        sum = 0
        for i in rew:
            sum += i.rating
        result = sum/all_rew
        context['rewiew'] = result
        return context


class DetailAuthor(DetailView):
    model = Author
    template_name = 'detail_author.html'
    context_object_name = 'detail'

