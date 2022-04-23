from django.db import models, transaction
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart',
                             verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время появления товара на сайте')
    price = models.PositiveIntegerField(default=0, verbose_name='цена')

    @property
    def product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.cart.select_related()

    def total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    @staticmethod
    def get_item(pk):
        return Cart.objects.filter(id=pk).first()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
            else:
                self.product.quantity -= self.quantity
            self.product.save()
            super(self.__class__, self).save(*args, **kwargs)

    @transaction.atomic  # Сохранить всё или ничего, аналогично с записью with transaction.atomic():
    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete(*args, **kwargs)
