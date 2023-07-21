import graphene
from graphene_django import DjangoObjectType
from .models import ShortenedURL
from .utils import generate_short_url


class ShortenedURLType(DjangoObjectType):
    class Meta:
        model = ShortenedURL


class Query(graphene.ObjectType):
    shortened_urls = graphene.List(ShortenedURLType)
    shorten_url = graphene.Field(ShortenedURLType, short_code=graphene.String())

    def resolve_shortened_urls(self, info, **kwargs):
        return ShortenedURL.objects.all()

    def resolve_shorten_url(self, info, **kwargs):
        short_code = kwargs.get("short_code")
        if short_code is not None:
            return ShortenedURL.objects.get(short_code=short_code)
        return None


class CreateShortenedURL(graphene.Mutation):
    class Arguments:
        original_url = graphene.String()

    url = graphene.Field(ShortenedURLType)
    message = graphene.String()

    def mutate(self, info, original_url):
        existing_url = ShortenedURL.objects.filter(original_url=original_url).first()
        if existing_url:
            return CreateShortenedURL(url=existing_url, message="URL already exists")

        short_code = generate_short_url(original_url)
        shortened_url = ShortenedURL.objects.get(short_code=short_code)
        return CreateShortenedURL(
            create_shortened_url=shortened_url, message="URL created successfully"
        )


class UpdateShortenedURL(graphene.Mutation):
    class Arguments:
        short_code = graphene.String()
        is_active = graphene.Boolean()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, **kwargs):
        short_code = kwargs.get("short_code")
        is_active = kwargs.get("is_active")

        try:
            shortened_url = ShortenedURL.objects.get(short_code=short_code)
            shortened_url.is_active = is_active
            shortened_url.save()
            return UpdateShortenedURL(success=True, message="URL updated successfully")
        except ShortenedURL.DoesNotExist:
            return UpdateShortenedURL(success=False, message="URL not found")
        except Exception as e:
            return UpdateShortenedURL(success=False, message=str(e))


class Mutation(graphene.ObjectType):
    create_shortened_url = CreateShortenedURL.Field()
    update_shortened_url = UpdateShortenedURL.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
