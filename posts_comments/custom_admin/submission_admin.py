from django.contrib import admin

from posts_comments.models import Solution


class SubmissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Solution._meta.fields]
