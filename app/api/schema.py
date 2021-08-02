import graphene
from graphene_django import DjangoObjectType

from library.models import Book
from library.services import get_book_by_params


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        exclude = ('id',)


class Query(graphene.ObjectType):
    get_books_by_params = graphene.List(BookType, title=graphene.String(required=False),
                                        subtitle=graphene.String(required=False),
                                        author=graphene.String(required=False),
                                        categories=graphene.String(required=False),
                                        publication_date=graphene.String(required=False),
                                        publisher=graphene.String(required=False),
                                        description=graphene.String(required=False))

    def resolve_get_books_by_params(root, info, title=None, subtitle=None, author=None, categories=None,
                                    publication_date=None, publisher=None, description=None):
        return get_book_by_params(title=title, subtitle=subtitle, author=author, categories=categories,
                                  publication_date=publication_date, publisher=publisher, description=description)


schema = graphene.Schema(query=Query)