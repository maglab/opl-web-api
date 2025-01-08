from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]


admin.site.register(Category, CategoryAdmin)
