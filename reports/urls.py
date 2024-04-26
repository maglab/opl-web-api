from django.urls import path
from views import GeneralReportView, OpenProblemReportView

url_patterns = [
    (
        path("/", GeneralReportView.as_view()),
        path("open-problem", OpenProblemReportView.as_view()),
    )
]
