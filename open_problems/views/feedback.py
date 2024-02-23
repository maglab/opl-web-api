from rest_framework.generics import ListCreateAPIView

from ..models.feedback import Report
from ..serializers.serializers import ReportSerializer


class ReportView(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
