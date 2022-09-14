from django.contrib import admin
from .models import Order, OrderItem, Customer, Cart, CartProduct, User, Contact


class OrderItemInline(admin.TabularInline):
    model = OrderItem



class OrderAdmin(admin.ModelAdmin):
    model = Customer
    inlines = [OrderItemInline]

admin.site.register(Order) #OrderAdmin)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(User)
admin.site.register(Contact)
# Register your models here.
