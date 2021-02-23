from django.contrib import admin
from django.contrib.admin import AdminSite, sites
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from easy_select2 import select2_modelform, apply_select2
from ckeditor.widgets import CKEditorWidget

from .models.user import User
# Register your models here.

# Custom site admin

class ShouAdminSite(AdminSite):
    site_header = _('Admin site for Shou.com')
    site_title = _('Hello from Shou with love')
    index_title = _('Shou.com')


admin_site = ShouAdminSite(name='Shou.com admin')
admin.site = admin_site
sites.site = admin_site
admin_site.register(User)