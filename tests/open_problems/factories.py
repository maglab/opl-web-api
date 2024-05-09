from factory.django import DjangoModelFactory
from factory import SubFactory, post_generation
from faker import Faker
from typing import Any, Iterable, Optional
from open_problems.models import OpenProblem, SubmittedOpenProblem
from ..users.factories import ContactFactory
from ..annotations.factories import (
    TagFactory,
    GeneFactory,
    SpeciesFactory,
    CompoundFactory,
)
from ..references.factories import ReferenceFactory

fake = Faker()


class AbstractProblemFactory(DjangoModelFactory):
    title: str = fake.text(max_nb_chars=200)
    description: str = fake.text(max_nb_chars=500)
    contact = SubFactory(ContactFactory)

    @post_generation
    def references(self, create: bool, extracted: Iterable[Any], **kwargs):
        if not create:
            return  # Only proceed if we're actually creating the instance (i.e., saving it to the database)
        if extracted is None:
            # Create default references if none are extracted
            extracted = [ReferenceFactory.create() for _ in range(2)]
        self.references.add(*extracted)

    @post_generation
    def tags(self, create: bool, extracted: Iterable[Any], **kwargs):
        if not create:
            return
        if extracted is None:
            extracted = [TagFactory.create() for _ in range(3)]

        self.tags.add(*extracted)

    @post_generation
    def compounds(self, create: bool, extracted: Iterable[Any], **kwargs):
        if not create:
            return
        if extracted is None:
            extracted = [CompoundFactory.create() for _ in range(2)]

        self.compounds.add(*extracted)

    @post_generation
    def genes(self, create: bool, extracted: Iterable[Any], **kwargs):
        if not create:
            return
        if extracted is None:
            extracted = [GeneFactory.create() for _ in range(4)]

        self.genes.add(*extracted)

    @post_generation
    def species(self, create: bool, extracted: Iterable[Any], **kwargs):
        if not create:
            return
        if extracted is None:
            extracted = [SpeciesFactory.create() for _ in range(2)]

        self.species.add(*extracted)


class OpenProblemFactory(AbstractProblemFactory):
    class Meta:
        model = OpenProblem

    is_active = True


class SubmittedOpenProblemFactory(AbstractProblemFactory):
    class Meta:
        model = SubmittedOpenProblem

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    organisation = fake.company()
    job_field = fake.job()
    notify_user = False
