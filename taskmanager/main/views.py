from django.shortcuts import render,redirect
from .models import Manga,Customer,CartProduct,Cart
from django import views
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import DetailView,View
from .forms import LoginForm,RegistrationForm
from django.contrib.auth import authenticate,login
from .mixins import CartMixin

def MainPage(request):
    mangas=Manga.objects.all()
    return render(request,"main/MainPage.html",{'books':mangas})

def AboutUs(request):
    return render(request,"main/AboutUs.html")


def Cart(request):
    return render(request,"main/cart.html")


class AlbumDetailView(views.generic.DetailView):
    model=Manga



class LoginView(views.View):
    def get(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        context={
            'form':form
        }
        return render(request,'main/login1.html',context)

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return HttpResponseRedirect('/')
            context={
                'form':form
            }
            return render(request,'main/registration.html',context)

class RegistrationView(views.View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST or None)
        context={
            'form':form
        }
        return render(request,'main/registration.html')

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=form.cleaned_data['username']
            new_user.email=form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone']
            )
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,user)
            return HttpResponseRedirect('/')
        context={
            'form':form
        }
        return render(request,'main/registration.html',context)


class AccountView(CartMixin,views.View):
    def get(self,request,*args,**kwargs):
        customer=Customer.objects.get(user=request.user)
        context={
            'customer':customer,
            'cart':self.cart
        }
        return render(request,'main/account.html',context)