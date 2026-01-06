# core/views.py
from django.shortcuts import render, redirect
from .forms import ClassDefinitionForm, UpdateForm


def define_class(request):
    if request.method == "POST":
        form = ClassDefinitionForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            attrs = [a.strip() for a in form.cleaned_data["attributes"].split(",")]
            fields = {a: "" for a in attrs}
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

    if request.method == "POST":
        form = UpdateForm(request.POST, instance=attributes)
        if form.is_valid():
            for attr, value in form.cleaned_data.items():
                attributes[attr] = value
            request.session["attributes"] = attributes
            return redirect("view_instance")
    else:
        form = UpdateForm(instance=attributes)

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
