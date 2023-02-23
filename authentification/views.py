from django.shortcuts import render, HttpResponse, redirect
from .forms import CreateUserForm, AuthForm, ProfileCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

def signin(request):
    if request.user.is_authenticated:
        return redirect('news')
    else:
        if request.method == 'POST':
            userform = AuthForm(data=request.POST)
            if userform.is_valid():
                # username = userform.cleaned_data['username']
                email = userform.cleaned_data['email']
                password = userform.cleaned_data['password']

                try:
                    # check is there user with such email
                    user = User.objects.get(email=email)
                    auth_user = authenticate(username=user.username, password=password)

                    if auth_user is not None:
                        login(request, auth_user)
                        return redirect('news')
                    else:
                        messages.error(request, 'Incorrect email or password!')
                        return render(request, template_name='authentification/signin.html', context={'form': userform})
                except:
                    messages.error(request, 'Incorrect email or password!')
                    return render(request, template_name='authentification/signin.html', context={'form': userform})

                # auth_user = authenticate(username=user.username, email=email)
                # if auth_user is not None:
                #     login(request, auth_user)
                #     return redirect('news')
                # else:
                #     return render(request, template_name='authentification/signin.html', context={'form': userform})
            else:
                return render(request, template_name='authentification/signin.html', context={'form': userform})
        else:
            userform = AuthForm()
            return render(request, template_name='authentification/signin.html', context={'form': userform})


def signup(request):
    # block the url if the user is authenticated
    if request.user.is_authenticated:
        return redirect('news')
    else:
        if request.method == 'POST':
            userform = CreateUserForm(request.POST)
            profileform = ProfileCreationForm(request.POST, request.FILES)

            if userform.is_valid() and profileform.is_valid():
                user = userform.save()
                user.profile.avatar = profileform.cleaned_data['avatar']
                user.save()
                # Create profile for just created user
                # profile = profileform.save(commit=False)
                # profile.user = user


                username = user.username
                messages.success(request, f'Account created succesfully for {username}')
                # login if registered successfully
                auth_user = authenticate(username=username, password=userform.cleaned_data['password2'])
                login(request, auth_user)
                return redirect('news')
            else:
                return render(request, template_name='authentification/signup.html', context={'userform': userform, 'profileform': profileform})
        else:
            userform = CreateUserForm()
            profileform = ProfileCreationForm()
            return render(request, template_name='authentification/signup.html', context={'userform': userform, 'profileform': profileform})


def signout(request):
    logout(request)
    return redirect('signin')
