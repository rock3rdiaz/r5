import traceback
from typing import List, Dict, Any

from django.db import IntegrityError

from book_client.services import GoogleClient
from library.models import Book

google_client = GoogleClient()


def get_book_by_params(**kwargs):
    """
    Detect and return books founded using params received
    """
    if kwargs.get('title', None):
        return get_book_by_title(kwargs['title'])
    if kwargs.get('subtitle', None):
        return get_book_by_subtitle(kwargs['subtitle'])
    if kwargs.get('author', None):
        return get_book_by_author(kwargs['author'])
    if kwargs.get('categories', None):
        return get_book_by_categories(kwargs['categories'])
    if kwargs.get('publication_date', None):
        return get_book_by_publication_date(kwargs['publication_date'])
    if kwargs.get('publisher', None):
        return get_book_by_publisher(kwargs['publisher'])
    if kwargs.get('description', None):
        return get_book_by_description(kwargs['description'])


def save_external_info(data: List[Dict[str, Any]]) -> None:
    """
    Save external book inside internal db
    """
    for d in data['items']:
        try:
            Book.objects.create(title=d['volumeInfo']['title'], subtitle=d['volumeInfo'].get('subtitle', None),
                                author=','.join(d['volumeInfo']['authors']),
                                categories=[','.join(d['volumeInfo']['categories']) if d['volumeInfo'].get('categories',
                                                                                                           None) else None][
                                    0],
                                publication_date=d['volumeInfo'].get('publishedDate', None),
                                publisher=d['volumeInfo'].get('publisher', None), description=d['volumeInfo'].get('description', None),
                                image=[d['volumeInfo']['imageLinks']['thumbnail'] if d['volumeInfo'].get('imageLinks',
                                                                                                         None) and
                                                                                     d['volumeInfo']['imageLinks'].get(
                                                                                         'thumbnail', None) else None][
                                    0])
        except IntegrityError:
            print(f'------- IntegrityError error => {traceback.format_exc()}')


def get_book_by_title(title: str) -> Book:
    """
    Return a Book by 'title' property
    """
    try:
        books = Book.objects.filter(title__icontains=title.strip())
        if books.count() == 0:
            data = google_client.get_books_by_params(title.strip(), 'intitle')
            save_external_info(data)
        return Book.objects.filter(title__icontains=title.strip())
    except KeyError:
        print(f'------- key error => {traceback.format_exc()}')


def get_book_by_subtitle(subtitle: str) -> Book:
    """
    Return a Book by 'subtitle' property
    """
    try:
        books = Book.objects.filter(subtitle__icontains=subtitle.strip())
        if books.count() == 0:
            data = google_client.get_books_by_params(subtitle.strip(), 'intitle')
            save_external_info(data)
        return Book.objects.filter(subtitle__icontains=subtitle.strip())
    except KeyError:
        print(f'------- key error => {traceback.format_exc()}')


def get_book_by_author(author: str) -> Book:
    """
    Return a Book by 'author' property
    """
    try:
        books = Book.objects.filter(author__icontains=author.strip())
        if books.count() == 0:
            data = google_client.get_books_by_params(author.strip(), 'inauthor')
            save_external_info(data)
        return Book.objects.filter(author__icontains=author.strip())
    except KeyError:
        print(f'------- key error => {traceback.format_exc()}')


def get_book_by_categories(categories: str) -> Book:
    """
    Return a Book by 'categories' property
    """
    books = Book.objects.filter(categories__icontains=categories.strip())
    if books.count() == 0:
        data = google_client.get_books_by_params(categories.strip(), 'subject')
        save_external_info(data)
    return Book.objects.filter(categories__icontains=categories.strip())


def get_book_by_publication_date(publication_date: str) -> Book:
    """
    Return a Book by 'publication_date' property
    """
    return Book.objects.filter(publication_date=publication_date.strip())


def get_book_by_publisher(publisher: str) -> Book:
    """
    Return a Book by 'publisher' property
    """
    books = Book.objects.filter(publisher__icontains=publisher.strip())
    if books.count() == 0:
        data = google_client.get_books_by_params(publisher.strip(), 'inpublisher')
        save_external_info(data)
    return Book.objects.filter(publisher__icontains=publisher.strip())


def get_book_by_description(description: str) -> Book:
    """
    Return a Book by 'description' property
    """
    books = Book.objects.filter(description__icontains=description.strip())
    if books.count() == 0:
        data = google_client.get_books_by_params(description.strip(), '')
        save_external_info(data)
    return Book.objects.filter(description__icontains=description.strip())
