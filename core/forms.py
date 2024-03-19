from django import forms
from django.apps import apps

# Generate choices for all models
MODEL_CHOICES = [
    (model._meta.label, model._meta.verbose_name_plural) for model in apps.get_models()
]


class JsonModelUploadForm(forms.Form):
    model = forms.ChoiceField(choices=MODEL_CHOICES, label="Select Model")
    json_file = forms.FileField(label="Upload JSON File")
