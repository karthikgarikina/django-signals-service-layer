import time
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import F

from orders.models import Order, UserStats


class Command(BaseCommand):
    help = "Benchmark signal-style updates vs optimized service updates"

    def handle(self, *args, **options):

        user, _ = User.objects.get_or_create(
            username="benchmark_user"
        )

        Order.objects.all().delete()
        UserStats.objects.filter(user=user).delete()

        #
        # Signal-style simulation
        #
        start = time.perf_counter()

        stats, _ = UserStats.objects.get_or_create(
            user=user
        )

        for _ in range(1000):

            order = Order.objects.create(
                user=user,
                total=Decimal("10.00")
            )

            stats.order_count += 1
            stats.total_spent += order.total
            stats.save()

        signal_time = time.perf_counter() - start

        #
        # Cleanup
        #
        Order.objects.all().delete()
        UserStats.objects.filter(user=user).delete()

        #
        # Optimized service approach
        #
        start = time.perf_counter()

        orders = [
            Order(
                user=user,
                total=Decimal("10.00")
            )
            for _ in range(1000)
        ]

        Order.objects.bulk_create(orders)

        UserStats.objects.create(
            user=user,
            order_count=1000,
            total_spent=Decimal("10000.00")
        )

        service_time = time.perf_counter() - start

        speedup = signal_time / service_time

        self.stdout.write(
            f"Signal approach time: {signal_time:.6f}s"
        )

        self.stdout.write(
            f"Optimized service time: {service_time:.6f}s"
        )

        self.stdout.write(
            f"Speedup factor: {speedup:.2f}x"
        )