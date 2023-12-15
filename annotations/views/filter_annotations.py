from django.apps import apps

from open_problems.models.open_problems import OpenProblems


def filter_by_annotations(annotations):
    query_set = OpenProblems.objects.all()

    for annotation_name, annotation_value in annotations.items():
        try:
            # Retrieve the model dynamically based on the annotation name
            annotation_model = apps.get_model("annotations", annotation_name)
            # Check if the model name is the same as the annotation name
            if annotation_model.__name__ == annotation_name:
                intermediary_model = apps.get_model(
                    "annotations", f"{annotation_name}problem"
                )
                intermediary_related_name = f"{annotation_name.lower()}problem"
                intermediary_filter = {intermediary_related_name: annotation_value}
                intermediary_results = intermediary_model.objects.filter(
                    **intermediary_filter
                )
                # Get the primary keys of the OpenProblems related to the filtered intermediary results
                open_problem_ids = [
                    result.open_problem_id_id for result in intermediary_results
                ]
                # Filter the 'query_set' based on the primary keys of OpenProblems
                query_set = query_set.filter(id__in=open_problem_ids)
        except KeyError:
            raise KeyError(f"Invalid annotation name: {annotation_name}")

    return query_set
