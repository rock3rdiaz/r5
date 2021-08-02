import graphene
import graphql_jwt
from graphene_django import DjangoObjectType

from library.models import Book
from library.services import get_book_by_params, remove_book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        exclude = ('id',)


class Query(graphene.ObjectType):
    get_books_by_params = graphene.List(BookType, title=graphene.String(required=False),
                                        subtitle=graphene.String(required=False),
                                        author=graphene.String(required=False),
                                        category=graphene.String(required=False),
                                        publication_date=graphene.String(required=False),
                                        publisher=graphene.String(required=False),
                                        description=graphene.String(required=False))

    def resolve_get_books_by_params(root, info, title=None, subtitle=None, author=None, category=None,
                                    publication_date=None, publisher=None, description=None):
        return get_book_by_params(title=title, subtitle=subtitle, author=author, category=category,
                                  publication_date=publication_date, publisher=publisher, description=description)


class BookMutator(graphene.Mutation):
    class Arguments:
        identifier = graphene.UUID(required=True)

    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, identifier):
        message = remove_book(identifier)
        return BookMutator(message=message)


class BookMutation(graphene.ObjectType):
    remove_book = BookMutator.Field()


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Mutation(BookMutation, AuthMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
