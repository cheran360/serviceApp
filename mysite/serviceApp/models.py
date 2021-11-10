from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
class Service(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  _id = models.AutoField(primary_key=True, editable=False)
  name = models.CharField(max_length=200, null=True, blank=True)
  about = models.TextField(null=True, blank=True)
  feasiblelocations = models.CharField(max_length=200, null=True, blank=True)
  rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
        
  def __str__(self):
    return self.name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)