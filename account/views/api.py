from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from rest_framework_simplejwt.tokens import RefreshToken

from utils import data_from_method_post_put_delete

from main.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from account.models import ActivateAccountToken
from django.utils.timezone import now
from main.models.location_signed_in import LocationSignedIn
from rest_framework.authtoken.models import Token


@swagger_auto_schema(
    method='post',
    operation_description='test send mail',
    operation_summary='test send mail',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(description='email', type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_EMAIL),
        }
    ),
    responses={
        HTTP_200_OK: openapi.Response(
            description='',
            examples={
                'status': 'Email sent successfully'
            }
        ),
        HTTP_400_BAD_REQUEST: openapi.Response(
            description='',
            examples={
                'status': 'Email was not provided'
            }
        ),
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_send_mail(request, email=None):
    reply_to = settings.DEFAULT_FROM_EMAIL
    send_mail(
        'subject: TEST EMAIL SHOU',
        'message: test email',
        reply_to,
        ['duondg@gmail.com'],
        fail_silently=False,
    )
    return Response(data="success", status=HTTP_200_OK)
 

#========================== CLASSES BASE VIEWS =======================

class Login(APIView):

    def post(self, request):
        
        email, password = data_from_method_post_put_delete(request, 'email', 'password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                ip = Login.get_client_ip(request)
                device = request.headers.get('User-Agent')
                last_login = now()
                LocationSignedIn.objects.create(
                    device=device,
                    # location=f"{response.get('city')}, {response.get('country_code')}",
                    ip=ip,
                    last_login=last_login, user=user)
                data = {
                    'status': 'success',
                    'user_id': user.id,
                    '_token': user.auth_token.key,
                    'user_url': user.url,
                    'jwt_token': Login.get_jwt_token_for_user(user)
                }
                return Response(data=data, status=HTTP_200_OK)
            raise Exception('Wrong password or email', 400)
            
        except (User.DoesNotExist, Exception) as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': 'Failed', 'message': f'{msg}'},
                        status=code if code else HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_client_ip(request):
        # Get Ip address of login user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_jwt_token_for_user(user: User) -> dict:
        # Return jwt serializer for user
        refresh = RefreshToken.for_user(user)
        # For more claim just user refresh['key'] = value
        refresh['email'] = user.email
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class Logout(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Đăng xuất',
        operation_summary='Đăng xuất',
        responses={
            HTTP_200_OK: openapi.Response(
                description='',
                examples={
                    'status': 'true'
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        Token.objects.get(user_id=request.user.id).delete()
        Token.objects.create(user=request.user)
        return Response(data={'status': True}, status=HTTP_200_OK)

class Register(APIView):
    """Create new account"""
    @swagger_auto_schema(
        operation_summary='API đăng kí tài khoản',
        operation_description='Đăng kí tài khoản trong hệ thống',
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            'repeat_password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
        }),
        responses={
            HTTP_201_CREATED: openapi.Response(
                description='Success', examples={
                    'status': 'success',
                    'message': {'activated': 'False'}
                }
            ),
            HTTP_400_BAD_REQUEST: openapi.Response(
                description='Success', examples={
                    'status': 'success',
                    'message': 'String'
                }
            )
        }
    )
    def post(self, request, *arg, **kwargs):
        try:
            first_name, last_name, email, password, repeat_password = data_from_method_post_put_delete(
                request, 'first_name', 'last_name', 'email', 'password', 'repeat_password'
            )
            # Check if the email already exists in the system 
            if User.objects.filter(email__iexact=str(email).lower()).exists():
                raise Exception('Email already existed', 302)
            # check repeat password
            if password != repeat_password:
                raise Exception('Repeat password does not matched for password', 400)
            # create new user 
            user = User(first_name=first_name, last_name=last_name, email=str(email).lower(),
                        is_active=False, is_superuser=False)
            user.set_password(password)
            user.save()

            # send an account activation email
            token = ActivateAccountToken.objects.get(user=user)
            subject = "Xác thực tài khoản Shou.com của bạn"
            domain = get_current_site(request)
            body = render_to_string('account/email/mail_activate.html', {'user': user, 'domain': domain, 'token': token})
            reply_to = settings.DEFAULT_FROM_EMAIL
            request_activate_mail = EmailMessage(subject=subject, body=body, to=[email], reply_to=[reply_to])
            request_activate_mail.content_subtype = 'html'
            request_activate_mail.send(fail_silently=True)
            
            return Response(data={'status': 'Success', 'message': {'activated': 'False'}},
                            status=HTTP_201_CREATED)

        except Exception as e:
            if len(e.args) == 2:
                msg, code = e.args
            else:
                msg, code = e.args, None
            return Response(data={'status': 'Failed', 'message': f'{msg}'},
                            status=code if code else HTTP_400_BAD_REQUEST)



