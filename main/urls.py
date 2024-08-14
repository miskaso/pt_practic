from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.DetailBook.as_view(), name='book'),
    path('author/<int:pk>/', views.DetailAuthor.as_view(), name='author'),
    path('review/<int:book_id>', views.add_review, name='add_review'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_author/', views.add_author, name='add_author'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)