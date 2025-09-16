from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemsForms
from .models import ShopAtSinItem
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    items = ShopAtSinItem.objects.all()

    context = {
        "app_name": "ShopAtSin",              
        "student_name": "Annisa Muthia Alfahira",  
        "student_class": "F"   ,
        'items': items
    }

    return render(request, "main.html", context)


def create_item(request):
    form = ItemsForms(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_item.html", context)


def show_item(request, id):
    item = get_object_or_404(ShopAtSinItem, pk=id)

    context = {
        'item': item
    }

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
