from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from main.models import ShopAtSinItem

class ItemsForms(ModelForm):
    class Meta:
        model = ShopAtSinItem
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured", "stock", "brand", "rating"]


class RegistrationForm(UserCreationForm):
    username = UsernameField(
        max_length=25,
        help_text="Required. 25 characters or fewer. Letters, digits and @/./+/-/_ only.",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
