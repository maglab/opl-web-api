from django.apps import apps
from django.views import View
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import JsonModelUploadForm
import json


@method_decorator(staff_member_required, name="dispatch")
class JSONImportView(View):
    template_name = "admin/json_upload.html"
    form_class = JsonModelUploadForm
    success_url = "admin:index"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                json_file = request.FILES["json_file"]
                data = json.load(json_file)  #

                app_label, model_name = form.cleaned_data.get("model").split(".")
                # This assumes that the table names follow the django naming convention
                try:
                    model = apps.get_model(app_label=app_label, model_name=model_name)
                except LookupError:
                    raise Http404("Model not found")

                for item in data:
                    instance, created = model.objects.get_or_create(**item)
                    if created:
                        instance.save()
                return redirect(self.success_url)
            except json.JSONDecodeError:
                form.add_error("json_file", "Invalid JSON file")
            except (
                Exception
            ) as e:  # General exception, ideally you should handle more specific exceptions
                form.add_error(None, f"Unexpected error occurred: {str(e)}")

        return render(request, self.template_name, {"form": form})
