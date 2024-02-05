from django.contrib import admin

from posts_comments.models.Post import PostReferences


# Customm admin class for Submissions and their references
class SubmissionReferenceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostReferences._meta.fields]
