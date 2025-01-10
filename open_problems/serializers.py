from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)
from open_problems.models import Contact, SubmittedOpenProblem, OpenProblem
from references.serializers import ReferenceSerializer
from references.models import Reference
from annotations.serializers import (
    TagSerializer,
    GeneSerializer,
    CompoundsSerializer,
    SpeciesSerializer,
)
from users.serializers import ContactSerializer
from annotations.models import Tag, Gene, Compound, Species
from categories.serializers import CategorySerializer


# Serializer for parent node of open problem
class ParentChildSerializer(ModelSerializer):
    class Meta:
        model = OpenProblem
        fields = ["title", "problem_id", "description"]


class OpenProblemsSerializer(ModelSerializer):
    contact = ContactSerializer()
    children = ParentChildSerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    solution_count = SerializerMethodField()
    discussion_count = SerializerMethodField()
    parent_problem = ParentChildSerializer()
    tags = TagSerializer(many=True, read_only=True)
    genes = GeneSerializer(many=True, read_only=True)
    compounds = CompoundsSerializer(many=True, read_only=True)
    species = SpeciesSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = OpenProblem
        fields = [
            "problem_id",
            "title",
            "description",
            "contact",
            "parent_problem",
            "references",
            "descendants_count",
            "solution_count",
            "children",
            "discussion_count",
            "tags",
            "genes",
            "compounds",
            "species",
            "categories",
        ]

    @staticmethod
    def get_solution_count(obj):
        return obj.solution.filter(is_active=True).count()

    @staticmethod
    def get_discussion_count(obj):
        return obj.discussion.filter(is_active=True).count()


# Separate serializers for fetching and posting.
class SubmittedOpenProblemSerializer(ModelSerializer):
    contact = ContactSerializer()
    references = ReferenceSerializer(many=True)
    tags = TagSerializer(many=True)
    genes = GeneSerializer(many=True)
    compounds = CompoundsSerializer(many=True)
    species = SpeciesSerializer(many=True)

    class Meta:
        model = SubmittedOpenProblem
        fields = "__all__"


class SubmittedOpenProblemPostSerializer(ModelSerializer):
    contact = PrimaryKeyRelatedField(queryset=Contact.objects.all(), allow_null=True)
    references = PrimaryKeyRelatedField(many=True, queryset=Reference.objects.all())
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    genes = PrimaryKeyRelatedField(many=True, queryset=Gene.objects.all())
    compounds = PrimaryKeyRelatedField(many=True, queryset=Compound.objects.all())
    species = PrimaryKeyRelatedField(many=True, queryset=Species.objects.all())

    class Meta:
        model = SubmittedOpenProblem
        fields = "__all__"
