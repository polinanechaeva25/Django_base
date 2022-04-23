from django.db import models, transaction
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class OrderItemQuerySet(models.QuerySet):
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


class Order(models.Model):
    FORMING = '1'
    SENT_TO_PROCEED = '2'
    PROCEEDED = '3'
    PAID = '4'
    READY = '5'
    CANCEL = '6'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'обрабатывается'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'собирается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='действительность', db_index=True, default=True)

    def __str__(self):
        return f'Текущий заказ: {self.pk}'

    # @cached_property
    # def get_items_cached(self):
    #     return self.orderitems.select_related()
    #
    # # @property
    # def get_total_quantity(self):
    #     items = self.get_items_cached
    #     return sum(list(map(lambda x: x.quantity, items)))
    #
    # # @property
    # def get_total_cost(self):
    #     items = self.get_items_cached
    #     return sum(list(map(lambda x: x.get_products_cost, items)))

    # переопределяем метод, удаляющий объект
    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    @property
    def get_products_cost(self):
        return self.product.price * self.quantity
