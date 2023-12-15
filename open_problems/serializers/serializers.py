from utils.base_serializer import BaseSerializer
from ..models.open_problems import (
    Contact,
    OpenProblems,
    ProblemReference,
    SubmittedProblems,
)
from ..models.references import Reference


# Serializer for parent node of open problem
class ParentSerializer(BaseSerializer):
    class Meta:
        model = OpenProblems


class ContactSerializer(BaseSerializer):
    class Meta:
        model = Contact


# Serializer for user submitted open problems
class SubmittedProblemSerializer(BaseSerializer):
    # converted_references = serializers.SerializerMethodField()

    class Meta:
        model = SubmittedProblems


# Serializer to return a reference to be nested in serializer below
class ReferenceSerializer(BaseSerializer):
    class Meta:
        model = Reference


# For all references for a particular open problem
class FilterReferenceSerializer(BaseSerializer):
    reference = ReferenceSerializer(source="reference_id")

    class Meta:
        model = ProblemReference
