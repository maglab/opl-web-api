from django.urls import path, include
from rest_framework import routers


from annotations.views import (
    CompoundViewSet,
    GeneViewSet,
    SpeciesViewSet,
    TagViewSet,
)


# Register routers the viewsets

router = routers.DefaultRouter()
viewsets = {
    "gene": GeneViewSet,
    "tag": TagViewSet,
    "species": SpeciesViewSet,
    "compound": CompoundViewSet,
}

for route, viewset in viewsets.items():
    router.register(route, viewset, basename=route)

# Create a list of prefixes for the viewsets for urls to be dynamically generated

# Base url api/annotations/
urlpatterns = [
    path("", include(router.urls)),
]
