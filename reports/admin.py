from django.contrib import admin
from .models import GeneralReport, OpenProblemReport

# Register your models here.

admin.site.register(GeneralReport)
admin.site.register(OpenProblemReport)
