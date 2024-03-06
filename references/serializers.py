from rest_framework.serializers import ModelSerializer

from open_problems.models import Reference


class ReferenceSerializer(ModelSerializer):
    class Meta:
        model = Reference
        fields = "__all__"
