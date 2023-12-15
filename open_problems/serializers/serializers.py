import json

from rest_framework import serializers

from utils.get_doi_information import doi_crossref_search
from utils.get_pmid_information import get_pmid_citation
from utils.recursive_serializer import RecursiveSerializer

from ..models.open_problems import (
    Contact,
    OpenProblems,
    ProblemReference,
    SubmittedProblems,
)
from ..models.references import Reference


# Serializer for parent node of open problem
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenProblems
        fields = ["problem_id", "title"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name"]


# Serializer for reviewed open problems
class OpenProblemsSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = OpenProblems
        fields = [
            "problem_id",
            "title",
            "description",
            "contact",
            "parent_problem",
            "descendants_count",
            "children",
        ]


# Serializer for user submitted open problems
class SubmittedProblemSerializer(serializers.ModelSerializer):
    # converted_references = serializers.SerializerMethodField()

    class Meta:
        model = SubmittedProblems
        fields = [
            "problem_id",
            "title",
            "description",
            "species",
            "references",
            "parent_problem",
            "first_name",
            "last_name",
            "email",
            "organisation"
        ]




# Serializer to return a reference to be nested in serializer below
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = "__all__"


# For all references for a particular open problem
class FilterReferenceSerializer(serializers.ModelSerializer):
    reference = ReferenceSerializer(source="reference_id")

    class Meta:
        model = ProblemReference
        fields = ["reference"]
