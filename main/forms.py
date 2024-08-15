from django import forms
from .models import Review, Book, Author
from django.core.exceptions import ValidationError
import datetime
import os


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, label='Выбрать '
                                                                'оценку')

    class Meta:
        model = Review
        fields = ['rating', 'text']
        labels = {
            'text': 'Ваш отзыв'
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Запишите ваш отзыв'}),
        }


class AddBookForm(forms.ModelForm):

    public_year = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': (datetime.date.today() - datetime.timedelta(
                days=1)).strftime('%Y-%m-%d'),
            'placeholder': 'Выберите дату'
        }),
        input_formats=['%Y-%m-%d'], label='Дата'
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'desc', 'public_year']

        labels = {
            'title': 'Заголовок',
            'author': 'Автор',
            'desc': 'Описание'
        }
        widgets = {
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Добавьте описание книги'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Добавьте название книги'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Добавьте название книги'
            })
        }

    def clean_public_year(self):
        date_str = self.cleaned_data['public_year']
        if isinstance(date_str, datetime.date):
            return date_str
        return datetime.datetime.strptime(date_str, '%d.%m.%Y').date()


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        labels = {
            'name': 'Имя автора',
            'bio': 'Биография'
        }

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Заполните '
                                                         'биографию автора'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя автора'
            })
        }
