from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from main.models import User
from account.models import ActivateAccountToken

def create_activate_token(sender, **kwargs):
    """
    Khi một user được tạo ra signal sẽ được kích hoạt như vậy sẽ tạo được activate token
    :param sender:
    :param kwargs:
    :return:
    """
    if kwargs.get('created'):
        ActivateAccountToken.objects.create(user=kwargs.get("instance"))
        # Tạo token cho user để xác thực rest_framework
        Token.objects.create(user=kwargs.get('instance'))


# Kết nối signal và hàm reciever
post_save.connect(receiver=create_activate_token, sender=User)