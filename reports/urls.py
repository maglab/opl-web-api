from django.urls import path
from .views import GeneralReportView, OpenProblemReportView

urlpatterns = [
    path("", GeneralReportView.as_view()),
    path("open-problem", OpenProblemReportView.as_view()),
]
