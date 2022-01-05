from django.db.models.signals import pre_save
from django.dispatch import receiver
from .tasks import create_profile,update_profile
from .models import AllUser


@receiver(pre_save,sender=AllUser)
def create_profile_signals(sender,instance,**kwargs):
    create_profile(instance)

    



@receiver(pre_save,sender=AllUser)
def update_profile_signals(sender,instance,**kwargs):
    update_profile(instance)
    