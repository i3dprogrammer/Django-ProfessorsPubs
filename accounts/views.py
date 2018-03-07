from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from p_profile.models import ProfessorProfile


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return self.process(request, request.user)
        return render(request, 'accounts/login.html', {}) #TODO

    def post(self, request):
        if request.user.is_authenticated:
            return self.process(request, request.user)

        post_username = request.POST.get('username')
        post_password = request.POST.get('password')

        user = authenticate(username=post_username, password=post_password)

        return self.process(request, user)

    def process(self, request, user):
        if user is None:
            context = {
                'error':'Invalid login credentials!',
            }
            return render(request, 'accounts/login.html', context) #TODO

        login(request, user)

        if ProfessorProfile.objects.filter(user=user).exists():
            return redirect('p_profile:view')
        else:
            return redirect('p_profile:create')
