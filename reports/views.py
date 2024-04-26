from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from serializers import GeneralReportSerializer, OpenProblemReportSerializer
from models import GeneralReport, OpenProblemReport

# Create your views here.


class GeneralReportView(CreateAPIView):
    serializer_class = GeneralReportSerializer
    queryset = GeneralReport.objects.all()


class OpenProblemReportView(CreateAPIView):
    serializer_class = OpenProblemReportSerializer
    queryset = OpenProblemReport.objects.all()
