import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemsForms, RegistrationForm
from .models import ShopAtSinItem
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get('filter', 'all')

    context = {
        "app_name": "ShopAtSin",
        "student_name": "Annisa Muthia Alfahira",
        "student_class": "F",
        "last_login": request.COOKIES.get('last_login', 'Never'),
        "filter_type": filter_type,  # optional: bisa dipakai buat highlight tombol filter
    }
    return render(request, "main.html", context)


@login_required(login_url='/login')
def create_item(request):
    form = ItemsForms(request.POST or None)

    if form.is_valid() and request.method == "POST":
        # sesuai tutorial: commit=False lalu isi field user
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return redirect("main:show_main")

    context = {"form": form}
    return render(request, "create_item.html", context)


@login_required(login_url='/login')
def show_item(request, id):
    item = get_object_or_404(ShopAtSinItem, pk=id)
    context = {"item": item}
    return render(request, "item_detail.html", context)


def show_xml(request):
    data = ShopAtSinItem.objects.all()
    xml = serializers.serialize("xml", data)
    return HttpResponse(xml, content_type="application/xml")


def show_json(request):
    data = ShopAtSinItem.objects.all()
    js = serializers.serialize("json", data)
    return HttpResponse(js, content_type="application/json")


def show_xml_by_id(request, id):
    obj = get_object_or_404(ShopAtSinItem, pk=id)
    xml = serializers.serialize("xml", [obj])  # iterable
    return HttpResponse(xml, content_type="application/xml")


def show_json_by_id(request, id):
    obj = get_object_or_404(ShopAtSinItem, pk=id)
    js = serializers.serialize("json", [obj])
    return HttpResponse(js, content_type="application/json")


def _serialize_item(item, user):
    return {
        "id": item.pk,
        "name": item.name,
        "price": item.price,
        "description": item.description,
        "thumbnail": item.thumbnail,
        "category": item.category,
        "is_featured": item.is_featured,
        "stock": item.stock,
        "brand": item.brand,
        "rating": item.rating,
        "date_added": item.date_added.isoformat() if item.date_added else None,
        "is_owner": item.user == user or user.username == "admin",
        "detail_url": reverse("main:show_item", args=[item.pk]),
    }


@login_required(login_url='/login')
@require_http_methods(["GET"])
def fetch_items(request):
    filter_type = request.GET.get("filter", "all")
    query = ShopAtSinItem.objects.all()
    if filter_type == "my":
        query = query.filter(user=request.user)

    items = [_serialize_item(item, request.user) for item in query.order_by("-pk")]
    return JsonResponse({"items": items})


@login_required(login_url='/login')
@require_http_methods(["POST"])
def create_item_ajax(request):
    form = ItemsForms(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return JsonResponse(
            {"message": "Product created successfully.", "item": _serialize_item(item, request.user)},
            status=201,
        )

    return JsonResponse({"message": "Invalid data.", "errors": form.errors}, status=400)


def register(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "message": "Your account has been successfully created!",
                        "redirect_url": reverse('main:login'),
                    },
                    status=201,
                )
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {"message": "Please correct the errors below.", "errors": form.errors},
                status=400,
            )

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(request, data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)

        redirect_url = reverse("main:show_main")
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            response = JsonResponse(
                {"message": "Login successful.", "redirect_url": redirect_url}
            )
        else:
            messages.success(request, "Login successful.")
            response = HttpResponseRedirect(redirect_url)

        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

      if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "message": "Login failed. Please check your credentials.",
                "errors": form.errors,
            },
            status=400,
        )

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)


def logout_user(request):
    messages.success(request, "You have logged out.")
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
def edit_item(request, id):
    item = get_object_or_404(ShopAtSinItem, pk=id)
    # hanya pemilik yang boleh edit
    if item.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this item.")

    form = ItemsForms(request.POST or None, instance=item)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, "Item updated.")
        return redirect('main:show_item', id=item.pk)

    return render(request, 'edit_item.html', {'form': form, 'item': item})

@login_required(login_url='/login')
@require_POST
def delete_item(request, id):
    item = get_object_or_404(ShopAtSinItem, pk=id)
    # hanya pemilik yang boleh delete

    if item.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this item.")
    
    item.delete()
    messages.success(request, "Item deleted.")
    return HttpResponseRedirect(reverse('main:show_main'))


@login_required(login_url='/login')
@require_http_methods(["POST"])
def update_item_ajax(request, id):
    item = get_object_or_404(ShopAtSinItem, pk=id)
    if item.user != request.user:
        return JsonResponse({"message": "You are not allowed to edit this item."}, status=403)

    form = ItemsForms(request.POST or None, instance=item)
    if form.is_valid():
        item = form.save()
        return JsonResponse(
            {"message": "Product updated successfully.", "item": _serialize_item(item, request.user)}
        )

    return JsonResponse({"message": "Invalid data.", "errors": form.errors}, status=400)


@login_required(login_url='/login')
@require_http_methods(["POST"])
def delete_item_ajax(request, id):
    item = get_object_or_404(ShopAtSinItem, pk=id)
    if item.user != request.user:
        return JsonResponse({"message": "You are not allowed to delete this item."}, status=403)

    item.delete()
    return JsonResponse({"message": "Product deleted successfully."}, status=200)
