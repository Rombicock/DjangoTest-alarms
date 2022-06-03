from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models


class Alarm(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    time = models.TimeField('Alarm time')
    active = models.BooleanField()

    def __str__(self):
        func = {
            True: 'active',
            False: ''
        }
        return f'{self.time} {func[self.active]}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)