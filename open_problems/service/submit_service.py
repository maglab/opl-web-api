from django.db import models
from rest_framework.exceptions import ParseError
from typing import Protocol, Type, List, Union, Any
from dataclasses import dataclass, field, asdict

from references.service.reference_service import retrieve_references
from users.service import get_or_create_contact
from core.service.service import get_or_create_instances
from annotations.models import Tag, Gene, Compound, Species


# Using a dataclass to encapsulate submission data with clear type annotations
@dataclass
class SubmitDataclass:
    title: str
    description: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    organisation: str = ""
    job_field: str = ""
    contact: int = None
    notify_user: bool = False
    references: List[dict] = field(default_factory=list)
    tags: List[Union[str, dict]] = field(default_factory=list)
    compounds: List[Union[str, dict]] = field(default_factory=list)
    species: List[Union[str, dict]] = field(default_factory=list)
    genes: List[Union[str, dict]] = field(default_factory=list)


# Protocol for an instance converter
class InstanceConverter(Protocol):

    def convert(self, submit_data: SubmitDataclass) -> Any:
        """
        For converting serialized data into primary keys
        """


class ContactConverter(InstanceConverter):
    def __init__(self, creator: get_or_create_contact):
        self.contact_creator = creator

    def convert(self, submit_data: SubmitDataclass) -> Any:
        contact_data = asdict(
            submit_data,
            dict_factory=lambda x: {
                k: v
                for k, v in x
                if k
                in ["first_name", "last_name", "email", "organisation", "job_field"]
            },
        )
        return self.contact_creator(data=contact_data, return_pk=True)


class ReferencesConverter(InstanceConverter):
    def __init__(self, creator: retrieve_references):
        self.reference_creator = creator

    def convert(self, submit_data: SubmitDataclass) -> [Any]:
        return self.reference_creator(submit_data.references)


class AnnotationConverter(InstanceConverter):
    def __init__(
        self,
        creator: get_or_create_instances,
        annotation: str,
        model: Type[models.Model],
    ):
        self.annotation_model = model
        self.annotation_creator = creator
        self.annotation = annotation

    @staticmethod
    def clean_function(data: Union[dict, str]):
        if isinstance(data, str):
            return data
        for dict_key, value in data.items():
            if isinstance(value, dict):
                data[dict_key] = value["id"]
        return data

    def convert(self, submit_data: SubmitDataclass) -> [Any]:
        return self.annotation_creator(
            model=self.annotation_model,
            item_list=submit_data.__getattribute__(self.annotation),
            clean_function=self.clean_function,
        )


class SubmitOpenProblemService:
    dataclass = SubmitDataclass

    def __init__(self, request: dict):
        self.request_data = request

    def _set_up_data(self):
        try:
            data = self.dataclass(**self.request_data)
        except TypeError:
            raise ParseError()
        else:
            return data

    @staticmethod
    def _format_data(data: SubmitDataclass):
        formatted_references = ReferencesConverter(creator=retrieve_references).convert(
            submit_data=data
        )
        formatted_contact = ContactConverter(creator=get_or_create_contact).convert(
            data
        )
        formatted_tags = AnnotationConverter(
            creator=get_or_create_instances, annotation="tags", model=Tag
        ).convert(data)
        formatted_genes = AnnotationConverter(
            creator=get_or_create_instances, annotation="genes", model=Gene
        ).convert(data)
        formatted_species = AnnotationConverter(
            creator=get_or_create_instances, annotation="species", model=Species
        ).convert(data)
        formatted_compounds = AnnotationConverter(
            creator=get_or_create_instances, annotation="compounds", model=Compound
        ).convert(data)

        return {
            **asdict(data),
            "references": formatted_references,
            "contact": formatted_contact,
            "tags": formatted_tags,
            "genes": formatted_genes,
            "species": formatted_species,
            "compounds": formatted_compounds,
        }

    def send_email(self): ...

    def create(self):
        data = self._set_up_data()
        print(data)
        formatted_data = self._format_data(data)
        return formatted_data
