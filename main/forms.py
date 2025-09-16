from django.forms import ModelForm
from main.models import ShopAtSinItem

class ItemsForms(ModelForm):
    class Meta:
        model = ShopAtSinItem
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured", "stock", "brand", "rating"]