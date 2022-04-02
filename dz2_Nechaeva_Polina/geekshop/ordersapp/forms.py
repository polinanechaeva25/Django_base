from django import forms
from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemsForm(forms.ModelForm):

    price = forms.CharField(label='цена', required=True)

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderItemsForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['price'].initial = self.instance.product.price