from django.db import models

from .user import User

class LocationSignedIn(models.Model):
    """
    Information device login
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    device = models.CharField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=300,  blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shou_location_signed_in'