from django.contrib import admin

from .custom_admin.submission_admin import SubmissionAdmin
from .models import Solution, Comment


# Register your models here.
class CommentSubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ["full_text"]


admin.site.register(Comment)
admin.site.register(Solution, SubmissionAdmin)
