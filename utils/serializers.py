from rest_framework import serializers


class AllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
