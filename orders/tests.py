from django.test import TestCase
from .models import Order, Dish

class OrderTestCase(TestCase):
    def setUp(self):
        self.dish1 = Dish.objects.create(name="Борщ", price=300)
        self.dish2 = Dish.objects.create(name="Салат крабовый", price=320)
        self.order = Order.objects.create(table_number=1, total_price=620)
        self.order.dishes.add(self.dish1, self.dish2)

    def test_order_total_price(self):
        self.assertEqual(self.order.total_price, 620)