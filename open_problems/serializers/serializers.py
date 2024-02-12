from references.models import Reference
from utils.base_serializer import BaseSerializer
from ..models.open_problems import (
    Contact,
    OpenProblem,
    SubmittedOpenProblem,
)


# Serializer for parent node of open problem
class ParentSerializer(BaseSerializer):
    class Meta:
        model = OpenProblem


class ContactSerializer(BaseSerializer):
    class Meta:
        model = Contact


# Serializer for user submitted open problems
class SubmittedProblemSerializer(BaseSerializer):
    # converted_references = serializers.SerializerMethodField()

    class Meta:
        model = SubmittedOpenProblem


# Serializer to return a reference to be nested in serializer below
class ReferenceSerializer(BaseSerializer):
    class Meta:
        model = Reference
