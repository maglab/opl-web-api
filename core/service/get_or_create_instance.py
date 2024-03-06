def get_or_create_instance(model, parameters: dict):
    """
    Generic get or create instance function
    Args:
        model: Django Model. Model to get/create instances for
        parameters: dict - Dictionary of parameters to be unpacked.
    """
    model_instance, created = model.objects.get_or_create(**parameters)
    return model_instance, created
