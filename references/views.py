from django.db import models
from rest_framework.generics import ListAPIView

from .models import Reference
from .serializers import ReferenceSerializer


# Create your views here.


class ListReferencesView(ListAPIView):
    serializer_class = ReferenceSerializer

    def get_queryset(self):
        model_name = self.kwargs["model"]
        model_class = getattr(models, model_name, None)
        if model_class is None:
            # Handle case where model is not found
            return Reference.objects.none()

        instance_id = self.kwargs["pk"]
        try:
            instance = model_class.objects.get(pk=instance_id)
            return instance.references.all()
        except model_class.DoesNotExist:
            # Handle case where instance is not found
            return Reference.objects.none()
