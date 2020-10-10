from datetime import datetime

from rest_framework import viewsets, response, status
from rest_framework.decorators import action

from apps.orders.apis.serializers import OrderSerializer
from apps.orders.models import Order


def validate_serializer(data, instance=None):
    serializer = OrderSerializer(data=data, instance=instance, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(active=True).order_by('-creation_date')
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        data = self.queryset
        serializer = OrderSerializer(data, many=True, context={'request', request})
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data_create = request.data
        validate_serializer(data=data_create)
        user_id = data_create['user']
        data_orders = self.queryset.filter(user_id=user_id)
        serializer_orders = OrderSerializer(data_orders, many=True, context={'request': request})
        return response.Response(serializer_orders.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data_update = request.data
        validate_serializer(data=data_update, instance=instance)
        user_id = data_update['user']
        data_orders = self.queryset.filter(user_id=user_id)
        serializer_orders = OrderSerializer(data_orders, many=True, context={'request': request})
        return response.Response(serializer_orders.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='by_user/(?P<user_id>[0-9]+)/(?P<finish>(True|False))')
    def by_user(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        finish = self.kwargs.get('finish')
        data = self.queryset.filter(user_id=user_id, finish=finish)
        serializer = OrderSerializer(data, many=True, context={'request': request})
        return response.Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='finish_order/(?P<order_id>[0-9]+)')
    def finish_order(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        instance = self.queryset.filter(id=order_id).first()
        data_update = {"finish": True, "finish_date": datetime.now()}
        validate_serializer(data=data_update, instance=instance)
        data_orders = self.queryset.filter(finish=False)
        serializer_orders = OrderSerializer(data_orders, many=True, context={'request': request})
        return response.Response(serializer_orders.data)
