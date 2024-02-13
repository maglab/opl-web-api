from ..models import Reference


def create_reference_instance(reference_dictionary: dict):
    # The output of the doi / pmid converters should mirror the model fields
    reference_instance, created = Reference.objects.get_or_create(
        **reference_dictionary
    )
    return reference_instance
