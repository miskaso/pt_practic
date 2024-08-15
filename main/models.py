from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    desc = models.TextField()
    public_year = models.DateField()
    file = models.FileField()

    def __str__(self):
        return f"{self.title} {self.author}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    status = models.BooleanField()

    def __str__(self):
        return f'{self.book} {self.rating}'
