from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def calculate_total_price(sender, instance, **kwargs):
    """
    Сигнал для расчета общей стоимости заказа после сохранения.
    """
    if instance.dishes.exists():  # Проверяем, есть ли связанные блюда
        instance.total_price = sum(dish.price for dish in instance.dishes.all())
        # Отключаем сигнал на время сохранения
        post_save.disconnect(calculate_total_price, sender=Order)
        instance.save()  # Сохраняем объект
        post_save.connect(calculate_total_price, sender=Order)  # Включаем сигнал обратно