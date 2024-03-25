from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.core.mail import send_mail
import random
# Create your views here.


def index(request):
    return render(request , 'index.html')
def home(request):
    if request.user.is_anonymous:
        return redirect('/signin')
    return render(request, 'home.html')

# signin function 
def signin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request , username=username , password=password)
            print(user)
            if user is not None:
                login(request , user)
                return redirect('/home')
            else:
                return HttpResponse("Invalid user and password")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred while processing your request.")
    return render(request , 'signin.html')
# SignUp Function 
def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            ver_code = random.randint(1000, 9999)
            from_email = 'ex@ansqazzafi.com'
            subject = 'Registration Confirmation'
            message = f'Thank you for registering with us! Your verification code is: {ver_code}'
            recipient_list = [email]

            if password != cpassword:
                return HttpResponse("Passwords didn't match")
            elif User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists. Please choose a different one.")
            else:
                send_mail(subject, message, from_email, recipient_list)
                request.session['ver'] = ver_code
                request.session['user'] = username
                request.session['email'] = email
                request.session['password'] = password
                return redirect('/verification')
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred while processing your request.")
    return render(request, 'signup.html')

# Verification Function to verify the verification code
def verification(request):
    if request.method == 'POST':
        try:
            Uverification_code = request.POST.get('verification_code')
            ver_code = request.session.get('ver')
            username = request.session.get('user')
            email = request.session.get('email')
            password = request.session.get('password')
            if Uverification_code == str(ver_code):
                user = User.objects.create_user(username , email , password)
                user.save()
                print("user added success")
                return redirect('/signin')
            else:
                print("invalid")
                return redirect('/verification')
        except Exception as e:
            print("An error occurred:", e)
            return redirect('/verification')

    return render(request, 'verification.html')
def logoutUser(request):
    logout(request)
    return redirect('/signin')
