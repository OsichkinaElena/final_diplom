from django.contrib import admin
from .models import Order, OrderItem, Contact


class OrderItemInline(admin.TabularInline):
    model = OrderItem



class OrderAdmin(admin.ModelAdmin):
    model = Contact
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(Contact)
admin.site.register(OrderItem)
# Register your models here.
