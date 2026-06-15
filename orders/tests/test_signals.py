from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from orders.models import Order, UserStats
from orders.signals import update_user_stats_on_order_save


class SignalTests(TestCase):

    def setUp(self):
        post_save.connect(
            update_user_stats_on_order_save,
            sender=Order
        )

    def tearDown(self):
        post_save.disconnect(
            update_user_stats_on_order_save,
            sender=Order
        )

    def test_order_creation_updates_stats(self):
        user = User.objects.create_user(
            username="testuser",
            password="password"
        )

        Order.objects.create(
            user=user,
            total=100
        )

        stats = UserStats.objects.get(user=user)

        self.assertEqual(stats.order_count, 1)
        self.assertEqual(float(stats.total_spent), 100.00)
        
    def test_bulk_update_bypasses_signal(self):
        user1 = User.objects.create_user(
            username="user1",
            password="password"
        )

        user2 = User.objects.create_user(
            username="user2",
            password="password"
        )

        Order.objects.create(
            user=user1,
            total=100
        )

        stats = UserStats.objects.get(user=user1)

        self.assertEqual(stats.order_count, 1)

        orders = [
            Order(user=user2, total=50),
            Order(user=user2, total=60),
            Order(user=user2, total=70),
        ]

        Order.objects.bulk_create(orders)

        Order.objects.filter(
            user=user2
        ).update(user=user1)

        stats.refresh_from_db()

        self.assertEqual(stats.order_count, 1)
        self.assertEqual(float(stats.total_spent), 100.00)    