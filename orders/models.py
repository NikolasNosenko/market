from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product

ORDER_STATUS = (
    (1, 'Новый'),
    (2, 'В работе'),
    (3, 'Отклонено'),
    (4, 'Оплачено, ожидает доставки/ожидание клиента'),
    (5, 'Отменен'),
    (6, 'Завершен')
)

class Order(models.Model):
    customer_name = models.CharField(max_length=80)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    status = models.PositiveIntegerField(choices=ORDER_STATUS, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Заказ №%s: %s, %s' % (self.pk, self.customer_name, self.customer_phone)

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    count = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Товар %s в заказе №%s' % (self.product.product_name, self.order.pk)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.product.price
        super(ProductInOrder, self).save(*args, **kwargs)

@receiver(post_save, sender=ProductInOrder)
def save_order(sender, instance, created, **kwargs):
    total_price = 0
    products = ProductInOrder.objects.filter(order=instance.order)
    for prod in products:
        total_price+=prod.price*prod.count
    instance.order.total_price = total_price
    instance.order.save()