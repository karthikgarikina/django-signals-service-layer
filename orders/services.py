from django.db import transaction

from .models import Order, UserStats


def create_order(user, total):
    """
    Create an order and update user statistics
    within a single transaction.
    """

    with transaction.atomic():

        order = Order.objects.create(
            user=user,
            total=total
        )

        stats, _ = UserStats.objects.get_or_create(
            user=user
        )

        stats.order_count += 1
        stats.total_spent += order.total
        stats.save()

        return order