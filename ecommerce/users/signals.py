from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from ecommerce.order.models import Cart

User = get_user_model()

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    """
    Creates a new cart for a newly registered user.
    """
    if created:
        Cart.objects.create(user=instance)