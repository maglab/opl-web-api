from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get("context", {}).get("request")
        str_fields = request.GET.get("fields", "") if request else None
        fields = str_fields.split(",") if str_fields else None

        # Instantiate superclass normally
        super(BaseSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop the fields that are not specified in fields
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        fields = "__all__"
