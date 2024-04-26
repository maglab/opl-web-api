from rest_framework import serializers
from models import GeneralReport, OpenProblemReport


class GeneralReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralReport
        fields = "__all__"


class OpenProblemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenProblemReport
        fields = "__all__"
