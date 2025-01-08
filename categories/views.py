from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class ListCategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
