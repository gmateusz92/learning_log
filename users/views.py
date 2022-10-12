from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate ,logout # add to imports
from django.contrib.auth.forms import UserCreationForm
from . import forms


def register(request):
     """Rejestracja nowego użytkownika."""
     if request.method != 'POST':
        # Wyświetlenie pustego formularza rejestracji użytkownika.
        form = UserCreationForm()
     else:
        # Przetworzenie wypełnionego formularza.
        form = UserCreationForm(data=request.POST)
     if form.is_valid():
         new_user = form.save()
         # Zalogowanie użytkownika, a następnie przekierowanie go na stronę główną.
         authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
         login(request, authenticated_user)
         return redirect('index')
     context = {'form': form}
     return render(request, 'learning_logs/register.html', context)


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
            else:
                message = 'Login failed!'
    return render(request, 'learning_logs/login.html', {'form': form, 'message': message})

def logout_user(request):
    logout(request)
    return redirect('login_page')