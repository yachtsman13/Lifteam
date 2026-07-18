"""
Django signals для LiftTeam v2.2.
Сигналы используются только для:
- создания начальной записи истории статуса при создании заказа
- отправки WebSocket-уведомлений
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import RepairOrder, OrderStatusHistory, SparePart


@receiver(post_save, sender=RepairOrder)
def create_status_history(sender, instance, created, **kwargs):
    """Создание начальной записи истории при создании заказа."""
    if created:
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status,
            changed_at=timezone.now(),
            notes='Заказ создан'
        )


@receiver(post_save, sender=SparePart)
def notify_stock_update(sender, instance, created, **kwargs):
    """Отправка WebSocket-уведомления при изменении остатка детали."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "stock_updates",
        {
            "type": "stock_update",
            "data": {
                "part_id": instance.id,
                "part_number": instance.part_number,
                "name": instance.name,
                "current_stock": instance.current_stock,
                "min_stock": instance.min_stock,
                "is_below_min": instance.is_below_min_stock(),
            }
        }
    )
