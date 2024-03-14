from rest_framework.serializers import ModelSerializer

from references.models import Reference


class ReferenceSerializer(ModelSerializer):
    class Meta:
        model = Reference
        fields = "__all__"
