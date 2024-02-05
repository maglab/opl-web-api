from django.contrib import admin

from posts_comments.models.Post import Post


class SubmissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]
