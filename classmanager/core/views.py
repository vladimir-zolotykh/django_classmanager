from django.shortcuts import render, redirect
from django import forms
from .utils import create_class_instance


# Form to define a class
class ClassDefinitionForm(forms.Form):
    class_name = forms.CharField(label="Class Name")
    attributes = forms.CharField(label="Attributes (comma separated, e.g. name,age)")


# Form to update attributes
def make_update_form(instance):
    class UpdateForm(forms.Form):
        pass

    for attr in instance.__dict__:
        UpdateForm.base_fields[attr] = forms.CharField(
            initial=getattr(instance, attr), required=False
        )
    return UpdateForm


def define_class(request):
    if request.method == "POST":
        form = ClassDefinitionForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            attrs = [a.strip() for a in form.cleaned_data["attributes"].split(",")]
            fields = {a: "" for a in attrs}
            instance = create_class_instance(class_name, fields)
            request.session["class_name"] = class_name
            request.session["attributes"] = fields
            return redirect("update_instance")
    else:
        form = ClassDefinitionForm()
    return render(request, "define_class.html", {"form": form})


def update_instance(request):
    class_name = request.session.get("class_name")
    attributes = request.session.get("attributes")
    if not class_name or not attributes:
        return redirect("define_class")

    instance = create_class_instance(class_name, attributes)
    UpdateForm = make_update_form(instance)

    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            for attr, value in form.cleaned_data.items():
                attributes[attr] = value
            request.session["attributes"] = attributes
            return redirect("view_instance")
    else:
        form = UpdateForm()

    return render(
        request, "update_instance.html", {"form": form, "class_name": class_name}
    )


def view_instance(request):
    class_name = request.session.get("class_name")
    attributes = request.session.get("attributes")
    if not class_name or not attributes:
        return redirect("define_class")
    return render(
        request,
        "view_instance.html",
        {"class_name": class_name, "attributes": attributes},
    )
