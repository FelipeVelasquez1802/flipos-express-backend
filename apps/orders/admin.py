from django.contrib import admin

from apps.orders.models import Order


# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('format_cost', 'format_cost_order', 'description', 'user', 'creation_date', 'finish')
    list_display_links = list_display
