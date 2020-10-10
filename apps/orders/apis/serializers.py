from rest_framework import serializers

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'cost', 'cost_order', 'description', 'user', 'creation_date', 'finish_date', 'finish']
