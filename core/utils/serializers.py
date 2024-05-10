from rest_framework import serializers


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
