from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login, authenticate, logout

def home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')


    return render(request, 'login.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'User does not exist'})

        user = authenticate(email=email, password=password)
        if user is not None:
            
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        profession = request.POST.get('profession')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'User with this email already exists'})

        # Save the user to the database
        user = CustomUser(name=name, email=email, profession=profession)
        user.set_password(password)  # Use set_password to hash the password
        user.save()

        response = render(request, 'index.html')
        login(request, user)
        response.set_cookie('user', user.email)
        return response

def logout_view(request):
    logout(request)
    return redirect('home')


def plans(request):
    return redirect('home')

def analytics(request):
    return redirect('home')

def completed(request):
    return redirect('home')