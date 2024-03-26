from import_export import resources
from .models import OpenProblem


class OpenProblemResource(resources.ModelResource):
    class Meta:
        model = OpenProblem
