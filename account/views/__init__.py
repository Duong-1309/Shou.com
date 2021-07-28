from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import EmailMessage

from main.models import User
from account.models import ActivateAccountToken

class LoginView(View):
    login_template = 'account/login.html'

    def get(self, request, *args, **kwargs):
        try:
            auth_user_id = request.session['_auth_user_id']
            User.objects.get(id=auth_user_id)
            return redirect('/docs')
        except Exception:
            pass
        return render(request, self.login_template)
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            ip = request.META['REMOTE_ADDR']
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                login(request, user)
                request.session.set_expiry(3600)
                return redirect('/docs')
            raise ObjectDoesNotExist()
        except (ObjectDoesNotExist, Exception):
            messages.add_message(request, level=messages.INFO, extra_tags='alert alert-primary',
                                 message='Kiểm tra lại thông tin đăng nhập!')
            return redirect('account:login')

@require_POST
def register_account(request, *args, **kwargs):
    """
    Đăng kí tài khoản và nhận mail kích hoạt tài khoản
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    repeat_password = request.POST.get('repeat_password')
    if password != repeat_password:
        return redirect('account:register')

    user = User(first_name=first_name, last_name=last_name, email=str(email).lower())
    user.set_password(password)
    user.is_active = False
    user.is_superuser = False
    try:
        if User.objects.filter(email__iexact=str(email).lower()).exists():
            raise IntegrityError
        user.save()
    except IntegrityError:
        return redirect('account:register')
    
    token = ActivateAccountToken.objects.get(user=user)
    subject = "Xác thực tài khoản Shou.com của bạn"
    domain = get_current_site(request)
    body = render_to_string('account/email/mail_activate.html', {'user': user, 'domain': domain, 'token': token})
    reply_to = settings.DEFAULT_FROM_EMAIL
    request_activate_mail = EmailMessage(subject=subject, body=body, to=[email], reply_to=[reply_to])
    request_activate_mail.content_subtype = 'html'
    request_activate_mail.send(fail_silently=True)

    return render(request, 'account/register-success.html')

@require_GET
def activate_account(request, token=None):
    """
    Kích hoạt tài khoản dựa vào token gắn với mỗi thài khoản
    :param request:
    :param token: tương ứng với mỗi user
    :return:
    """
    try:
        activate_token = ActivateAccountToken.objects.get(token=token)
        # Kiểm tra thời hạn token
        user = User.objects.get(id=activate_token.user.id)
        user.is_active = True
        user.save()
        activate_token.delete()
        # Tạo cho user 1 profilesetting
    except ObjectDoesNotExist:
        return redirect(to='account:login')
    return render(request, 'account/account-activated.html', {'username': user.username})

def logout(request):
    return logout_then_login(request, login_url='/account/login')