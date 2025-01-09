from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class ListCategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RetrieveCategoryView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
