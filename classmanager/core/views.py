import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ClassDefinitionForm, UpdateForm, LoginForm
from .models import DynamicClass, DynamicInstance, AppUser


# --- Authorization helper ---
def require_login(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Basic "):
            # Ask for credentials
            response = HttpResponse("Authorization required", status=401)
            response["WWW-Authenticate"] = 'Basic realm="classmanager"'
            return response

        # Decode Basic Auth header
        try:
            encoded = auth_header.split(" ")[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
        except Exception:
            return HttpResponse("Invalid authorization header", status=400)

        # Check against DB
        try:
            user = AppUser.objects.get(username=username, password=password)
            request.user = user  # attach user to request
        except AppUser.DoesNotExist:
            return HttpResponse("Invalid credentials", status=401)

        return view_func(request, *args, **kwargs)

    return wrapper


# --- Optional login view (form-based) ---
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                AppUser.objects.get(username=username, password=password)
                # Normally you'd set a session, but with Basic Auth
                # you just instruct the user to send Authorization header.
                return HttpResponse("Login successful. Please use Basic Auth headers.")
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
