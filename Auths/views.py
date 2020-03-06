from django.shortcuts import render, redirect
from .forms import LoginForm, RegistForm
from .models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			username = cd['username']
			password = cd['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				if request.GET.get('next'):
					return redirect(request.GET['next'])
				if user.is_admin:
					return redirect('/admin')
				else:
					return redirect('/admin')
			else:
				form.add_error("username", "invalid")
				return render(request, 'auths/login.html', {'form': form})
	else :
		form = LoginForm()

	return render(request, 'auths/login.html', {'form': form})

@login_required
def logout_view(request):
	logout(request)
	return redirect('auths:login')
