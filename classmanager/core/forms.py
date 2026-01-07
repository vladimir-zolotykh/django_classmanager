from django import forms


class ClassDefinitionForm(forms.Form):
    class_name = forms.CharField(label="Class Name")
    attributes = forms.CharField(label="Attributes (comma separated)")


class UpdateForm(forms.Form):
    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        if instance is None:
            return
        for key, value in instance.values.items():
            self.fields[key] = forms.CharField(initial=value, required=False)
