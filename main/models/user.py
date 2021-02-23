from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now

from cloudinary.models import CloudinaryField

class User(AbstractUser):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=150,
        unique=False,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(blank=True, unique=True, help_text="Email address")
    picture = CloudinaryField('image', blank=True, null=True, help_text="File image")
    picture_url = models.URLField(blank=True, null=True, help_text="image url")
    url = models.CharField(max_length=300, blank=True, null=True, db_index=True, unique=True,
                           help_text='Địa chỉ tùy chỉnh đến trang cá nhân https://shou.com/user-url')

    class GenderChoice(models.TextChoices):
        MALE = 'male', _('MALE')
        FEMALE = 'female', _('FEMALE')
        OTHER = 'other', _('OTHER')
    
    gender = models.CharField(max_length=6, help_text="Giới tính", choices=GenderChoice.choices, blank=True, null=True)
    phone_num = models.CharField(max_length=12, help_text="phone number", blank=True, null=True, unique=True)
    last_modified = models.DateTimeField(help_text='date last modified', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """
        Ussername là họ và tên người dùng
        Url của user là slug của username
        :param args:
        :param kwargs:
        :return:
        """
        self.username = self.first_name + ' ' + self.last_name
        if self.url is None:
            self.url = slugify(self.username) + '-' + str(abs(hash(datetime.now())))
        self.last_modified = now()
        return super(User, self).save()

        def get_picture_url(self, width=50, height=50):
            return self.picture.build_url(secure=True, transformation=[
                {'width': width, 'height': height, 'crop': 'thumb'}
            ]) if self.picture is not None else None