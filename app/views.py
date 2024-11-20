from django.shortcuts import render, redirect
from .models import CustomUser, DayPlan, Task
from django.contrib.auth import login, authenticate, logout
from datetime import time
import json
from datetime import date 

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    
    user = request.user
    today = date.today()

    if DayPlan.objects.filter(user=user, date=today).exists():
        plan = DayPlan.objects.get(user=user, date=today)
        tasks = Task.objects.filter(DayPlan=plan)
        print(tasks)
    return render(request, 'index.html', {'tasks': tasks})

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
    return render(request, 'plan.html')

def analytics(request):
    return redirect('home')

def completed(request):
    return redirect('home')

def add_plan(request):
    if request.method =="POST":

        task_data = json.loads(request.POST.get('taskData'))
            
            # Extract data from the received JSON
        date = task_data.get('date')
        task = task_data.get('tasks', [])
        hour = task_data.get('hrs', [])
        minute = task_data.get('mins', [])
        category = task_data.get('categories', [])

        print(date, task, hour, minute, category)

        
        is_completed = False
        user = request.user

        if not date or not task or not category or not hour or not minute:
            return render(request, 'plan.html', {'error': 'All fields are required'})

        if not (len(task) == len(category) == len(hour) == len(minute)):
            return render(request, 'plan.html', {'error': 'Mismatched data in tasks, categories, or times.'})
    
        plan, created = DayPlan.objects.get_or_create(user=user, date=date)    
    
        Task.objects.filter(DayPlan=plan).delete()
        
        for tsk,ctgory,hr,mins in zip(task,category,hour,minute):
            print(hr, mins, tsk, ctgory)
            estimated_time = time(hour = int(hr), minute = int(mins))
            task = Task(DayPlan=plan, task=tsk, category=ctgory, estimated_time=estimated_time)
            task.save()
            print("task added")

        return render(request, 'plan.html', {'success': 'Plan added successfully'})

        
def get_plans(request):
    if request.method == 'GET':
        user = request.user
        date = request.GET.get('date')

        if not date:
            return render(request, 'plan.html', {'error': 'Date is required'})
        
        if DayPlan.objects.filter(user=user, date=date).exists():
            plan = DayPlan.objects.get(user=user, date=date)
            tasks = Task.objects.filter(DayPlan=plan)

            return render(request, 'index ')
        


        