from django import forms
from .models import Order, Dish

class OrderForm(forms.ModelForm):
    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Блюда'
    )

    class Meta:
        model = Order
        fields = ['table_number', 'dishes', 'status']