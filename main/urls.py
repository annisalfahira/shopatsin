from django.urls import path
from .views import (
    show_main,
    show_item,
    create_item,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
    fetch_items,
    create_item_ajax,
    update_item_ajax,
    delete_item_ajax,
)
from main.views import register, login_user, logout_user, edit_item, delete_item

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('items/<int:id>/', show_item, name='show_item'),
    path('items/create/', create_item, name='create_item'),

    path('items/<int:id>/edit/', edit_item, name='edit_item'),
    path('items/<int:id>/delete/', delete_item, name='delete_item'),

    path('items/xml/', show_xml, name='show_xml'),
    path('items/json/', show_json, name='show_json'),
    path('items/xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('items/json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('items/ajax/', fetch_items, name='fetch_items'),
    path('items/ajax/create/', create_item_ajax, name='create_item_ajax'),
    path('items/ajax/<int:id>/update/', update_item_ajax, name='update_item_ajax'),
    path('items/ajax/<int:id>/delete/', delete_item_ajax, name='delete_item_ajax'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
