from django.db import models
from typing import Type, Callable, List, Union, Dict
from dataclasses import dataclass, field, asdict
from references.service.reference_service import retrieve_references
from users.service import get_or_create_contact
from core.service.service import get_or_create_instances, return_pk, return_pk
from annotations.models import Tag, Gene, Compound, Species


# Using a dataclass to encapsulate submission data with clear type annotations
@dataclass
class SubmitDataClass:
    title: str
    description: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    organisation: str = ""
    job_field: str = ""
    contact: int = None
    references: List[dict] = field(default_factory=list)
    tags: List[Union[str, dict]] = field(default_factory=list)
    compounds: List[Union[str, dict]] = field(default_factory=list)
    species: List[Union[str, dict]] = field(default_factory=list)
    genes: List[Union[str, dict]] = field(default_factory=list)


class DataPreparationService:
    def __init__(
        self, submit_data: SubmitDataClass, data_creators: Dict[str, Callable]
    ):
        self.submit_data = submit_data
        self.data_creators = data_creators

    def prepare_contact_data(self):
        contact_data = asdict(
            self.submit_data,
            dict_factory=lambda x: {
                k: v
                for k, v in x
                if k
                in ["first_name", "last_name", "email", "organisation", "job_field"]
            },
        )
        return self.data_creators["contact"](contact_data)

    def prepare_references(self):
        return self.data_creators["reference"](self.submit_data.references)

    def prepare_model_instances(self, key: str, model: Type[models.Model]):
        # Nested data will be foreign keys, extract the ids
        def clean_function(data: dict | str):
            if isinstance(data, str):
                return data
            for dict_key, value in data.items():
                if isinstance(value, dict):
                    data[dict_key] = value["id"]
            return data

        return self.data_creators["instance"](
            model, getattr(self.submit_data, key), clean_function
        )

    def prepare_all_data(self):
        contact = self.prepare_contact_data()
        references = self.prepare_references()
        model_data = {
            "tags": Tag,
            "species": Species,
            "compounds": Compound,
            "genes": Gene,
        }
        model_instances = {
            key: self.prepare_model_instances(key, model)
            for key, model in model_data.items()
        }

        return {
            **asdict(self.submit_data),
            "contact": contact,
            "references": references,
            **model_instances,
        }


INSTANCE_CREATORS = {
    "contact": get_or_create_contact,
    "reference": retrieve_references,
    "instance": get_or_create_instances,
}


def set_up_data(request_data: dict):
    post_data = SubmitDataClass(**request_data)
    prepare_service = DataPreparationService(post_data, INSTANCE_CREATORS)
    prepared_data = prepare_service.prepare_all_data()
    contact = return_pk(prepared_data["contact"], None)
    references = [return_pk(reference, []) for reference in prepared_data["references"]]
    tags = [return_pk(tag, []) for tag in prepared_data.get("tags")]
    compounds = [return_pk(compound, []) for compound in prepared_data.get("compounds")]
    genes = [return_pk(gene, []) for gene in prepared_data.get("genes")]
    species = [return_pk(species, []) for species in prepared_data.get("species")]
    return {
        **prepared_data,
        "contact": contact,
        "references": references,
        "tags": tags,
        "compounds": compounds,
        "genes": genes,
        "species": species,
    }
