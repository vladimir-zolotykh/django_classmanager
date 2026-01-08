from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClassDefinitionForm, UpdateForm, LoginForm
from .models import DynamicClass, DynamicInstance, AppUser


# --- Authorization helper ---
def require_login(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = AppUser.objects.get(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                )
                request.session["user_id"] = user.id
                return redirect("define_class")
            except AppUser.DoesNotExist:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


# --- Protected views ---
@require_login
def define_class(request):
    if request.method == "POST":
        form = ClassDefinitionForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            attrs = [
                a.strip()
                for a in form.cleaned_data["attributes"].split(",")
                if a.strip()
            ]
            dyn_class = DynamicClass.objects.create(name=class_name, attributes=attrs)
            instance = DynamicInstance.objects.create(
                dynamic_class=dyn_class, values={a: "" for a in attrs}
            )
            return redirect("update_instance", pk=instance.pk)
    else:
        form = ClassDefinitionForm()
    return render(request, "define_class.html", {"form": form})


@require_login
def update_instance(request, pk):
    instance = get_object_or_404(DynamicInstance, pk=pk)
    if request.method == "POST":
        form = UpdateForm(request.POST, instance=instance)
        if form.is_valid():
            for attr, value in form.cleaned_data.items():
                instance.values[attr] = value
            instance.save()
            return redirect("view_instance", pk=instance.pk)
    else:
        form = UpdateForm(instance=instance)
    return render(
        request,
        "update_instance.html",
        {"form": form, "class_name": instance.dynamic_class.name},
    )


@require_login
def view_instance(request, pk):
    instance = get_object_or_404(DynamicInstance, pk=pk)
    return render(
        request,
        "view_instance.html",
        {
            "class_name": instance.dynamic_class.name,
            "attributes": instance.values,
            "instance": instance,
        },
    )
