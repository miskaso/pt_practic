from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, Review
from django.views.generic import DetailView, ListView, UpdateView
from django.core.paginator import Paginator
from .forms import ReviewForm, AddBookForm, AddAuthorForm
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

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
        rew = Review.objects.filter(book=book, status=True)
        if rew:
            print(len(rew))
            all_rew = len(rew)
            sum = 0
            for i in rew:
                sum += i.rating
            result = sum/all_rew
            context['rewiew'] = result
            return context
        else:
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
        review.status = False
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


class UpdateBook(UpdateView):
    model = Book
    fields = ['title', 'desc']
    template_name = 'update_book.html'

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.pk})


def delete_book(req, pk):
    if req.method == 'POST':
        book = get_object_or_404(Book, id=pk)
        book.delete()
        return redirect('home')
    else:
        return redirect('home')


class ReviewDetail(ListView):
    model = Review
    context_object_name = 'review'
    template_name = 'view_review.html'


def active_review(req, pk):
    model = get_object_or_404(Review, id=pk)

    if req.user.is_superuser:
        model.status = True
        model.save()
        messages.success(req, 'Вы одобрили отзыв'+model)
    else:
        messages.error(req, 'У вас нет прав на изменение статуса этого отзыва.')
    return redirect('review')


def del_review(req, pk):
    review = get_object_or_404(Review, id=pk)

    # Проверяем права доступа
    if req.user.is_superuser:
        review.delete()
        messages.success(req,
                         'Отзыв успешно удален.')
        return redirect('review')
    else:
        messages.error(req,
                       'У вас нет прав на удаление этого отзыва.')
        return redirect('review')


from django.db.models import Q
from django.shortcuts import render
from .models import Book

def get_search(request):
    data = request.GET.get('data', '')

    q_object = Q()

    if data:
        if data.isdigit():
            q_object |= Q(public_year__icontains=data)
        else:
            q_object |= Q(title__icontains=data) | Q(
                author__name__icontains=data)

    search_results = Book.objects.filter(q_object) if data else Book.objects.none()

    return render(request, 'search.html', {'search': search_results})
