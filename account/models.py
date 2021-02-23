import hashlib
import uuid
from django.utils.timezone import now

from django.db import models

from main.models.user import User

# chưa hiểu .cần nghiên cứu lại.. cre: hlnnox
def generate_token():
    """
    Tạo token bằng cách hash 224 uuid
    :return: 56 ký tự mã hóa
    """
    uid = str(uuid.uuid4())
    return hashlib.sha224(uid.encode(encoding='utf-8')).hexdigest()


class ActivateAccountToken(models.Model):
    """
        Token dùng để kích hoạt tài khoản, thời gian tồn tại của tài khoản
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, help_text="Mỗi user có nhiều token")
    token = models.CharField(max_length=56, default=generate_token, editable=False)
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return self.token
    