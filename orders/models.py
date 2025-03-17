from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField(verbose_name='Номер стола')
    dishes = models.ManyToManyField(Dish, verbose_name='Блюда')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус')

    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table_number})"

    def calculate_total_price(self):
        # Автоматический расчет общей стоимости на основе выбранных блюд
        self.total_price = sum(dish.price for dish in self.dishes.all())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)