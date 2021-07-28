from django.urls import path, include
from django.views.generic import RedirectView

app_name = 'main'

urlpatterns = [
     path('', RedirectView.as_view(url='/account/login')),
     path('chat/', include('chat.urls'))
]
