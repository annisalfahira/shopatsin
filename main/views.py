import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemsForms
from .models import ShopAtSinItem
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'all':
        items = ShopAtSinItem.objects.all()
    else:
        # contoh: ?filter=my  -> hanya item milik user login
        items = ShopAtSinItem.objects.filter(user=request.user)

    context = {
        "app_name": "ShopAtSin",
        "student_name": "Annisa Muthia Alfahira",
        "student_class": "F",
        "items": items,
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


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)


def logout_user(request):
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