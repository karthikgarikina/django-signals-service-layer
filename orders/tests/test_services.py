from django.test import TestCase
from django.contrib.auth.models import User

from orders.models import Order, UserStats
from orders.services import create_order


class ServiceLayerTests(TestCase):

    def test_create_order_service(self):

        user = User.objects.create_user(
            username="service_test_user",
            password="password"
        )

        order = create_order(
            user=user,
            total=100
        )

        self.assertIsInstance(order, Order)

        stats = UserStats.objects.get(
            user=user
        )

        self.assertEqual(
            stats.order_count,
            1
        )

        self.assertEqual(
            float(stats.total_spent),
            100.00
        )
        
        
    def test_order_creation_without_service_does_not_update_stats(self):

        user = User.objects.create_user(
            username="plain_order_user",
            password="password"
        )

        Order.objects.create(
            user=user,
            total=100
        )

        self.assertFalse(
            UserStats.objects.filter(user=user).exists()
        )        