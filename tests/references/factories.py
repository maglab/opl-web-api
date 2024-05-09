from factory.django import DjangoModelFactory
from factory import SubFactory, post_generation, Sequence
from faker import Faker
from faker.providers import isbn
from references.models import Author, Journal, Reference

fake = Faker()
fake.add_provider(isbn)


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = fake.name()


class JournalFactory(DjangoModelFactory):
    class Meta:
        model = Journal
        django_get_or_create = ["name"]

    name = Sequence(lambda n: f"{fake.name()}-{n}")


class ReferenceFactory(DjangoModelFactory):
    class Meta:
        model = Reference

    title = fake.text(max_nb_chars=150)
    citation = fake.text()
    doi = fake.isbn10(separator="-")
    pmid = fake.random_number(digits=8)
    year = fake.year()
    journal = SubFactory(JournalFactory)

    @post_generation
    def authors(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.authors.add(*extracted)
