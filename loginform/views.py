from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm,DivErrorList,EditProfileForm,ChangePasswordForm

def home(request):
	return render(request,'loginform/home.html',{})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		# User authentication to santizie authentication attempt, no RAW SQL queries #
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request,user)
			messages.success(request, ('You have successfully logged in!'))
			return redirect('home')
		else:
			messages.success(request, ('Login error - Please enter valid username and password.'))
			return redirect('login')

	else:
		return render(request,'loginform/login.html',{})	

def logout_user(request):
	logout(request)
	messages.success(request, ('You have been logged out successfully!'))		
	return redirect('home')

def register_user(request):
	if request.method == "POST":

		form = SignUpForm(request.POST,error_class=DivErrorList)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			# User authentication to santizie authentication attempt, no RAW SQL queries #
			user = authenticate(request, username=username, password=password)
			login(request,user)
			messages.success(request, ('You have successfully registered.'))
			return redirect('home')

	else:
		form = SignUpForm()

	context = {'form': form}
	return render(request,'loginform/register_user.html',context)

def edit_profile(request):
	if request.method == "POST":

		form = EditProfileForm(request.POST, instance=request.user, error_class=DivErrorList)
		if form.is_valid():
			form.save()
			messages.success(request, ('Profile changes have been saved.'))
			return redirect('home')

	else:
		form = EditProfileForm(instance=request.user)

	context = {'form': form}
	return render(request,'loginform/edit_profile.html',context)

def change_password(request):
	if request.method == "POST":

		form = ChangePasswordForm(data=request.POST, user=request.user, error_class=DivErrorList)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('Password has been changed.'))
			return redirect('home')

	else:
		form = ChangePasswordForm(user=request.user)

	context = {'form': form}
	return render(request,'loginform/change_password.html',context)

