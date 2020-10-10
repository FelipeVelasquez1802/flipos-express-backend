from django.db import models

from apps.users.models import User


# Create your models here.


def format_price(obj):
    return '${}'.format(obj)


class Order(models.Model):
    cost = models.IntegerField(verbose_name='Cost')
    cost_order = models.IntegerField(verbose_name='Order cost')
    description = models.TextField(verbose_name='Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    finish_date = models.DateTimeField(verbose_name='Finish date', null=True, blank=True)
    finish = models.BooleanField(verbose_name='Finish', default=False)
    cancel = models.BooleanField(verbose_name='Cancel', default=False)
    active = models.BooleanField(verbose_name='Active', default=True)

    @property
    def format_cost(self):
        return format_price(self.cost)

    @property
    def format_cost_order(self):
        return format_price(self.cost_order)

    def __str__(self):
        return 'Order number {} of {}'.format(self.id, self.user)
