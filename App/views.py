from django.shortcuts import HttpResponse, render, redirect
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.core.management import call_command
import os
# Create your views here.

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9 
    return ''.join(random.choices(characters, k=length))

def run_migrations(request):
    try:
        if os.environ.get("RENDER") == "true":  # Optional safety check
            call_command('migrate')
            return HttpResponse("Migrations applied!")
    except Exception as e:
        return HttpResponse(str(e))
    return HttpResponse("Not allowed", status=403)

def index(request):
    return render(request, 'index.html')

def about(request): 
    return render(request, 'About.html')

def login(request):
    if request.method == 'POST':
        phoneoremail = request.POST.get('phoneoremail')
        if phoneoremail.isnumeric():
            HttpResponse("Phone number is not available!")
        else:
            otp = str(random.randint(1000, 9999))
            subject = 'Hello from Hoichoi!'
            message = f'<#> Here\'s your Hoichoi Verification Code *| {otp} |* Enjoy Streaming now! *massage code={generate_random_string()}*'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [phoneoremail]
            
            send_mail(subject, message, from_email, recipient_list)

            request.session['phoneoremail'] = phoneoremail
            request.session['otp'] = otp

            return render(request, 'otp_verify.html', {'phoneoremail': phoneoremail})
    return render(request, 'login.html')

def otp_verify(request):
    if request.method == 'POST':
        phoneoremail = request.POST.get('phoneoremail')
        if phoneoremail:
            otp = request.POST.get('otp')
            print(otp)
            if otp == request.session.get('otp'):
                try:
                    if User.objects.filter(emailorphone=phoneoremail).exists():
                        massage = f'{phoneoremail} successfully logged in !'
                        return render(request, 'index.html', {'massages': massage})
                    else:
                        user = User(emailorphone=phoneoremail)
                        user.save()
                        return redirect('index')
                except Exception as e:
                    return HttpResponse(str(e))
            else:
                return HttpResponse("Invalid OTP!")
        else:
            return HttpResponse("Phone number is not available!")
            return render(request, 'login.html')
    return render(request, 'otp_verify.html')