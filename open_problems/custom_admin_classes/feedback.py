from django.contrib import admin


class ReportAdmin(admin.ModelAdmin):
    list_display = ["open_problem", "reason", "information"]
