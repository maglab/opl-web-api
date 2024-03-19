from django.contrib import admin

from .custom_admin.submission_admin import SubmissionAdmin
from .models import Solution, CommentSolution


# Register your models here.
class CommentSubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ["full_text"]


admin.site.register(CommentSolution)
admin.site.register(Solution, SubmissionAdmin)
