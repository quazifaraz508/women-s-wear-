from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from datetime import timedelta
from django.http import JsonResponse
# Create your views here.

def SignUP(request):
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        user_data_has_error = False
        
        if User.objects.filter(username = name).exists():
            user_data_has_error  = True
            messages.error(request, "Username already exists.")
        
        if User.objects.filter(email = email). exists():
            user_data_has_error  = True
            messages.error(request, "Email already exists.")
        
        if len(password) < 8:
            user_data_has_error  = True
            messages.error(request, "Password must be at least 8 characters long.")
        
        if user_data_has_error:
            return redirect('signup')
        else:
            new_user = User.objects.create_user(
                username = name,
                email = email,
                password = password,
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')
        
    return render(request, 'signup.html')
    
def LoginView(request):
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = name, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    
    return render(request, 'login.html')
def logoutView(request):
    logout(request)  # Log out the user
    next_url = request.META.get('HTTP_REFERER', '/')  # Fall back to home if no referrer
    return redirect(next_url)

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email = email)
            new_password_reset = PasswordReset(user= user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password',kwargs={'reset_id':new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            
            email_body  = f"Reset your password using the link below: \n\n\n{full_password_reset_url}"
            
            email_message = EmailMessage(
                'Password Reset',
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email_message.fail_silently = True
            email_message.send()
            return redirect('password-reset-sent', reset_id = new_password_reset.reset_id)
        
        except User.DoesNotExist:
            messages.error(request, "Email does not exist")
            return redirect('forgot-password')
        
    return render(request, 'forgot_password.html')


def PasswordResetSent (request, reset_id):
    
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
    return render(request, 'password_reset_sent.html')

def ResetPassword(request, reset_id):
    
    try:
        password_reset_id = PasswordReset.objects.get(reset_id = reset_id)
        
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            passwords_have_error = False
            
            if password != confirm_password:
                password_have_error = True
                messages.error(request, 'Password do not match')
            
            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password do not meet the requirements at least 5 characters long')
            
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)
            
            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)
    
    except PasswordReset.DoesNotExist:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
    
    return render(request, 'reset_password.html')


@login_required
def update_user_profile(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get("first_name", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()

        # Update fields
        user.first_name = first_name
        if hasattr(user, "phone_number"):  # if phone_number is on User model
            user.phone_number = phone_number
        elif hasattr(user, "profile"):  # if phone_number is in a profile model
            user.profile.phone_number = phone_number
            user.profile.save()

        user.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"})