from django.shortcuts import render

# Create your views here.

from django.views.generic import CreateView
from .models import CustomUser
from .models import User, OneTimeCode
from .forms import CustomUserCreationForm, AuthenticationForm, CodeLoginForm

from django.contrib.auth import authenticate, login

from django.shortcuts import redirect, render, HttpResponse
from .forms import AuthenticationForm

import random

class BaseRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = '/users/auth/'
    
    def form_valid(self, form):  
        new_user = form.save(commit=False)
        new_user.is_staff = 1
        new_user.save()    
        return super().form_valid(form)

def auth_user_view(request):
    print('--------- auth_user_view ---------')   
    if request.method=="POST":
#        print('request:', request)
#        print('valid request')
        form = AuthenticationForm(data = request.POST)
        email    = request.POST['email']
        password = request.POST['password']
        print('Entered email   :', email)
        print('Entered password:', password)
        user = authenticate(request, email=email, password=password)
#        print('user:', user)
        if user is not None:
            code = ''.join(random.choice('123456789') for i in range(4))
            OneTimeCode.objects.create(email=email, code=code)
#            print('code =', OneTimeCode.objects.last().code)          
            return redirect('/users/login/')
        else:
            return render(request,'auth.html',{'form':form,})
    else:
#        print('request:', request)
#        print('invalid request')
        form = AuthenticationForm()
        return render(request,'auth.html',{'form':form,})

def login_user_view(request):
    print('--------- login_user_view ---------')   
    if request.method=="POST":
#        print('request:', request)
#        print('valid request')
        form = CodeLoginForm(data = request.POST)
        email = request.POST['email']
        code  = request.POST['password']
        print('Entered email:', email)
        print('Entered code :', code)        
        if OneTimeCode.objects.filter(email=email, code=code).exists():
            print('Ура Ура Ура Ура Ура Ура Ура Ура ')
            user = User.objects.get(email=email)                  
            login(request, user)                   
            return redirect('/docs_work/')
        else:
            return render(request,'login.html',{'form':form,})
    else:
#        print('request:', request)
#        print('invalid request')
        form = CodeLoginForm()
        return render(request,'login.html',{'form':form,})





