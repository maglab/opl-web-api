import random

from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, Sequence
from faker import Faker
from annotations.models import Tag, Gene, Compound, Species

fake = Faker(["en_UK", "en_US", "en_PH"])


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    title = LazyAttribute(lambda x: fake.text(max_nb_chars=100))
    description = LazyAttribute(lambda x: fake.text())
    verified = True


class SpeciesFactory(DjangoModelFactory):
    class Meta:
        model = Species

    genus = LazyAttribute(lambda x: fake.first_name())
    species = LazyAttribute(lambda x: fake.last_name())
    full_name = LazyAttribute(lambda x: fake.name())
    ncbi_tax_id = fake.random_number(digits=random.randint(a=8, b=20))
    verified = True


class GeneFactory(DjangoModelFactory):
    class Meta:
        model = Gene

    name = LazyAttribute(lambda x: fake.text(max_nb_chars=50))
    gene_symbol = LazyAttribute(lambda x: fake.text(max_nb_chars=5))
    entrez_id = fake.random_number(digits=random.randint(a=8, b=20))
    species = SubFactory(SpeciesFactory)
    verified = True


class CompoundFactory(DjangoModelFactory):
    class Meta:
        model = Compound

    name = LazyAttribute(
        lambda x: fake.random_letters(length=10)
    )  # Need to match 100 chars
    chembl_id = Sequence(lambda n: 100000000 + n)
    pubchem_id = Sequence(lambda n: 100000001 + n)
    verified = True
