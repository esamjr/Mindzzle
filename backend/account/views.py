from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from .models import Profile

@require_http_methods(['GET','POST'])
def register(request):
    """
    user register new account

    :param request:
    :method POST:
    :return render register page
    """
    # check request method
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        # validate form
        if form.is_valid():
            form.save()
            # if data does not valid, return only username field
            username = form.cleaned_data.get('username')
            # message [success]
            messages.success(request, 'Your account has been created!')
            # Redirect to login-page
            return redirect('login/')

    # no requested data
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'auth/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    
        if  u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile': Profile.objects.get(user_account_name=request.user.id),
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'profile_page/profile.html', context)
    