from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, Review
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator
from .forms import ReviewForm, AddBookForm, AddAuthorForm

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


def add_review(request, book_id):
    form = ReviewForm(request.GET)
    if form.is_valid():
        review = form.save(commit=False)
        review.book = Book.objects.get(id=book_id)
        review.save()
        return redirect('book', pk=book_id)
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form})


def add_book(request):
    if request.user.username == 'admin':
        if request.method == 'POST':
            form = AddBookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = AddBookForm()

        return render(request, 'add_book.html', {'form': form})
    else:
        return redirect('home')


def add_author(request):
    if request.user.username == 'admin':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_book')
        else:
            form = AddAuthorForm()
            return render(request, 'add_author.html', {"form": form})
    else:
        return redirect('home')