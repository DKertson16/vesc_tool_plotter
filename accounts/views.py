from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			return redirect('accounts:login')

	context = {'form': form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
	next = ""
	if request.GET:
		next = request.GET['next']
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		print(next)
		if user is not None:
			login(request, user)
			if next == "":
				return redirect('/')
			else:
				return HttpResponseRedirect(next)
		else:
			messages.info(request, 'Username or Password is incorrect')
	context = {"next":next}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('/')
