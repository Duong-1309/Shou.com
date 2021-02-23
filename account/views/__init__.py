from django.views import View



class LoginView(View):
    login_template = 'account/login.html'

    def get(self, request, *args, **kwargs):
        pass