from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models.submissions import Submission, SubmittedReferences
# from .models.submissions import SubmissionReferences
from .serializers.submissions_serializer import SubmissionSerializer
# from .serializers.submissions_serializer import SubmissionReferences
from .serializers.submissions_serializer import SubmittedReferencesSerializer
from open_problems.models import OpenProblems
from .utils.parse_submitted_references import parse_submitted_references
# Create your views here.
# Getting the user submitted posts for a single open problem
@api_view(["GET"])
def get_posts(requests,id): 
    submissions_for_open_problem = Submission.objects.filter(open_problem=id, is_active=True)
    serializer = SubmissionSerializer(submissions_for_open_problem, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"]) #Doesn't work
def get_post(request, id): #Return single post 
    submission = Submission.objects.get(submission_id = id)
    sub_serializer = SubmissionSerializer(submission)

    #Check for submitted references: 
    references = SubmittedReferences.objects.filter(submission_id = id)
    ref_serializer = SubmittedReferencesSerializer(references, many=True)
    return Response({
        "post":sub_serializer.data, 
        "references":ref_serializer.data
    })

@api_view(["POST"])
def submit_post(request, id):
    if request.method == "POST": 
        serializer = SubmissionSerializer(data=request.data)
        open_problem = OpenProblems.objects.filter(question_id = id ).exists()

        if serializer.is_valid(raise_exception=True) & open_problem:
            serializer.save()
            # After saving parse the submitted serializer 
            reference_data = request.data["submitted_references"]
            if(reference_data):
                submission_id = serializer["submission_id"].value
                reference_list = parse_submitted_references(reference_data, submission_id)
                submitted_references_serializer = SubmittedReferencesSerializer(data=reference_list, many=True)
                if submitted_references_serializer.is_valid():
                    submitted_references_serializer.save()
                    print("saved")
                else:
                    print("invalid")
                    print(submitted_references_serializer.errors)
            

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
