import logging
import traceback
import uuid
from typing import List, Dict, Any, Tuple

from django.db import IntegrityError

from book_client.services import ExternalDataClient
from library.models import Book

logger = logging.getLogger(__name__)

external_client = ExternalDataClient()


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
    if kwargs.get('category', None):
        return get_book_by_category(kwargs['category'])
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
    books = []
    for item in data:
        # google's api results
        if item.get('items', None):
            for d in item['items']:
                b = Book(title=d['volumeInfo']['title'],
                         subtitle=d['volumeInfo'].get('subtitle', None),
                         author=[','.join(d['volumeInfo']['authors']) if d['volumeInfo'].get('authors', None) else None][0],
                         categories=[','.join(d['volumeInfo']['categories']) if d['volumeInfo'].get('categories',
                                                                                                    None) else None][
                             0],
                         publication_date=d['volumeInfo'].get('publishedDate', None),
                         publisher=d['volumeInfo'].get('publisher', None),
                         description=d['volumeInfo'].get('description', None),
                         image=
                         [d['volumeInfo']['imageLinks']['thumbnail'] if d['volumeInfo'].get('imageLinks', None) and
                                                                        d['volumeInfo']['imageLinks'].get(
                                                                            'thumbnail',
                                                                            None) else None][
                             0],
                         source='google')
                books.append(b)
        # ny times results
        if item.get('results', None):
            for d in item['results']:
                b = Book(title=d['book_title'],
                         subtitle=d['book_title'],
                         author=d['book_author'],
                         categories=None,
                         publication_date=d.get('publication_dt', None),
                         publisher=d.get('byline', None),
                         description=d.get('summary', None),
                         image=None,
                         source='ny-times')
                books.append(b)
    try:
        Book.objects.bulk_create(books)
    except IntegrityError:
        logger.error(f'------- IntegrityError error => {traceback.format_exc()}')


def get_book_by_title(title: str) -> Tuple[Book, str]:
    """
    Return a Book by 'title' property
    """
    books = Book.objects.filter(title__icontains=title.strip())
    if books.count() == 0:
        data = external_client.get_external_data(title.strip(), 'title')
        save_external_info(data)
        return Book.objects.filter(title__icontains=title.strip())
    __update_source(books)
    return books


def get_book_by_subtitle(subtitle: str) -> Book:
    """
    Return a Book by 'subtitle' property
    """
    books = Book.objects.filter(subtitle__icontains=subtitle.strip())
    if books.count() == 0:
        data = external_client.get_external_data(subtitle.strip(), 'title')
        save_external_info(data)
        return Book.objects.filter(subtitle__icontains=subtitle.strip())
    __update_source(books)
    return books


def __update_source(books: List[Book]) -> None:
    """
    Update books source to 'db'
    :param books: List of Books
    :return: None
    """
    for b in books:
        b.source = 'db'
    Book.objects.bulk_update(books, ['source'])


def get_book_by_author(author: str) -> Book:
    """
    Return a Book by 'author' property
    """
    books = Book.objects.filter(author__icontains=author.strip())
    if books.count() == 0:
        data = external_client.get_external_data(author.strip(), 'author')
        save_external_info(data)
        return Book.objects.filter(author__icontains=author.strip())
    __update_source(books)
    return books


def get_book_by_category(category: str) -> Book:
    """
    Return a Book by 'category' property
    """
    books = Book.objects.filter(categories__icontains=category.strip())
    if books.count() == 0:
        data = external_client.get_external_data(category.strip(), 'subject')
        save_external_info(data)
        return Book.objects.filter(categories__icontains=category.strip())
    __update_source(books)
    return books


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
        data = external_client.get_external_data(publisher.strip(), 'publisher')
        save_external_info(data)
        return Book.objects.filter(publisher__icontains=publisher.strip())
    __update_source(books)
    return books


def get_book_by_description(description: str) -> Book:
    """
    Return a Book by 'description' property
    """
    books = Book.objects.filter(description__icontains=description.strip())
    if books.count() == 0:
        data = external_client.get_external_data(description.strip(), '')
        save_external_info(data)
        return Book.objects.filter(description__icontains=description.strip())
    __update_source(books)
    return books


def remove_book(identifier: uuid) -> str:
    """
    Search and remove a Book
    :param identifier: Book's identificator
    :return:
    """
    try:
        Book.objects.get(identifier=identifier).delete()
        return 'book removed'
    except Book.DoesNotExist:
        logger.error(f' Book does not exist => {traceback.format_exc()}')
        return f'Book with identifier {identifier} does not exist!'
