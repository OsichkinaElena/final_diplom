from django.db import models
from account.models import User
from shop.models import ProductInfo, Product, Shop
from account.models import Contact
# Create your models here.

STATUS_CHOICES = (
    ('cart', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)



class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, verbose_name='Контакт', related_name='Контакт', blank=True, null=True,
                                on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, verbose_name='Статус', choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"
        ordering = ('-dt',)

    def __str__(self):
        return f'{self.user} - {self.dt}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)

    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', related_name='ordered_items',
                                     blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    total_amount = models.PositiveIntegerField(default=0, verbose_name='Общая стоимость')

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Список заказанных позиций"
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'product_info'], name='unique_order_item'),
        ]

    def __str__(self):
        return f'№ {self.order} - {self.product_info.model}. Кол-во: {self.quantity}. Сумма {self.total_amount} '

    def save(self, *args, **kwargs):
        self.total_amount = self.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)




# class Customer(models.Model):
#     user = models.OneToOneField('account.User', verbose_name="Пользователь", on_delete=models.CASCADE)
#     contact = models.ForeignKey('Contact', verbose_name="Контакт", on_delete=models.CASCADE)
#     orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order', blank=True)
#
#     def __str__(self):
#         if not (self.user.first_name and self.user.last_name):
#             return self.user.username
#         return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)
#

    # @property
    # def sum(self):
    #     return self.ordered_items.aggregate(total=Sum("quantity"))["total"]

# class Cart(models.Model):
#     products = models.ManyToManyField('CartProduct',  blank=True, related_name='carts')
#     total_products = models.PositiveIntegerField(default=0)
#     total_price = models.DecimalField(verbose_name='Сумма', decimal_places=2, max_digits=10)
#     owner = models.ForeignKey('Customer', verbose_name='Владелец', blank=True,
#                              on_delete=models.CASCADE)
#     for_anonymus_user = models.BooleanField(default=False)
#
#
#     def save(self, *args, **kwargs):
#         if self.id:
#             self.total_products = self.products.count()
#             self.total_price = sum([cproduct.total_price for cproduct in self.products.all()])
#         super().save(*args, **kwargs)
#
#
# class CartProduct(models.Model):
#     user = models.ForeignKey(User, verbose_name='Покупатель', blank=True,
#                              on_delete=models.CASCADE)
#     cart = models.ForeignKey('Cart', verbose_name='Корзина', blank=True, on_delete=models.CASCADE, )
#     product = models.ForeignKey(Product, verbose_name='Продукт', blank=True, on_delete=models.CASCADE)
#     price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10)
#     qty = models.PositiveIntegerField(default=1)
#     shop = models.ForeignKey(Shop, verbose_name='Магазин', blank=True,
#                              on_delete=models.CASCADE)
#
#     def save(self, *args, **kwargs):
#         self.price = self.qty * self.product.price
#         super().save(*args, **kwargs)