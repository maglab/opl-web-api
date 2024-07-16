from typing import Type, Any
from django.db import models
from django.http import HttpRequest


def get_or_create_instances(model, item_list: list, clean_function):
    instances = []
    for item in item_list:
        if isinstance(item, dict):
            clean_data = clean_function(item)
            instance, created = model.objects.get_or_create(**clean_data)
        else:
            continue
        instances.append(instance.pk)
    return instances


def return_serialized_data(model_instance, serializer):
    serializer = serializer(model_instance)
    return serializer.data


def return_pk(model_instance: Type[models.Model], default: Any):
    try:
        pk = model_instance.pk
    except AttributeError:
        return default
    return pk


def return_url(request: HttpRequest) -> dict:
    # Build the full URL
    scheme = request.scheme
    host = request.get_host()
    path = request.get_full_path()
    full_url = f"{scheme}://{host}{path}"

    return {"scheme": scheme, "host": host, "path": path, "full_url": full_url}
