from rest_framework.generics import ListAPIView

from references.serializers import ReferenceSerializer
from ..models.open_problems import OpenProblem


class ListReferencesView(ListAPIView):
    """
    List view to list all references for an open problem.
    """

    serializer_class = ReferenceSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        open_problem = OpenProblem.objects.get(pk=pk)
        return open_problem.references.all()
