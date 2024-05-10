from factory.django import DjangoModelFactory
from factory import SubFactory, Maybe, Iterator, LazyAttribute
from faker import Faker
from users.models import Contact, Organisation, JobField

fake = Faker()


class JobFieldFactory(DjangoModelFactory):
    class Meta:
        model = JobField

    title = LazyAttribute(lambda x: fake.job())


class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = Organisation

    title = LazyAttribute(lambda x: fake.company())


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    first_name = fake.first_name()
    last_name = fake.last_name()
    job_field = Maybe(
        "create_job_field",
        yes_declaration=SubFactory(JobFieldFactory),
        no_declaration=None,
    )
    organisation = Maybe(
        "create_organisation",
        yes_declaration=SubFactory(OrganisationFactory),
        no_declaration=None,
    )

    # You can control the creation of job_field and organisation with these parameters:
    create_job_field = Iterator([True, False])
    create_organisation = Iterator([True, False])

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        # Remove the control parameters before passing to the Contact constructor
        kwargs.pop("create_job_field", None)
        kwargs.pop("create_organisation", None)
        return kwargs
