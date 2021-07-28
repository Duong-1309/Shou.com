from django.urls import path, include
from account.views import api

urlpatterns = [
    path('api/', include([
        path('register/', api.Register.as_view(), name='api-register'),
        path('login/', api.Login.as_view(), name='api-login'),
        path('logout/', api.Logout.as_view(), name='api-logout'),
        # path('password/', include([
        #     path('forget/'),
        #     path('change/'),
        # ])),
        path('test-send-mail', api.test_send_mail, name='test-send-mail'),
    ]))
]
