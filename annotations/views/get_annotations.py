from rest_framework import status
from rest_framework.response import Response

from open_problems.models import OpenProblems


# Common logic for all the view.py files to extract annotations for a single open_problem
def get_annotation(id, Model, Serializer):
    open_problem = OpenProblems.objects.get(problem_id=id)
    if open_problem:
        attached_annotations = Model.objects.filter(open_problem=id)
        if attached_annotations:
            serializer = Serializer(attached_annotations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Getting annotation information for a particular annotation
def get_annotation_details(annotation_id, Model, Serializer):
    annotation = Model.objects.get(pk=annotation_id)
    if annotation:
        serializer = Serializer(annotation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
