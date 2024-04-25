from rest_framework.serializers import ModelSerializer
from references.models import Reference
from .service import ReferenceService


class ReferenceSerializer(ModelSerializer):
    class Meta:
        model = Reference
        fields = "__all__"
