from django.shortcuts import render, redirect
from .models import CustomUser, DayPlan, Task
from django.contrib.auth import login, authenticate, logout
from datetime import time
import json
from datetime import date 
from django.contrib import messages
from django.http import JsonResponse


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    
    user = request.user
    today = date.today()

    tasks = []


    progress = 0
    if DayPlan.objects.filter(user=user, date=today).exists():
        plan = DayPlan.objects.get(user=user, date=today)
        tasks = Task.objects.filter(DayPlan=plan)

        completed_time = (0, 0)
        total_time = (0, 0)
        
        for task in tasks:
            
            total_time= (total_time[0]+ task.estimated_time.hour, total_time[1] + task.estimated_time.minute) 
            if task.is_completed:
                completed_time = (completed_time[0]+ task.estimated_time.hour, completed_time[1]+task.estimated_time.minute)
        progress = (completed_time[0]*60 +completed_time[1])/(total_time[0]*60 + total_time[1])*100
        
    
    return render(request, 'index.html', {'tasks': tasks, 'progress': progress})

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
    if request.method == 'GET':
        user = request.user
        day = request.GET.get('date')
        
        if not day:
            day = date.today().strftime('%Y-%m-%d')

        tasks = []
        if DayPlan.objects.filter(user=user, date=day).exists():
            plan = DayPlan.objects.get(user=user, date=day)
            tasks = Task.objects.filter(DayPlan=plan)

            if day == str(date.today().strftime('%Y-%m-%d')):
                return render(request, 'completed.html', {'tasks': tasks, 'editable': True, 'date': day})
            else:
                return render(request, 'completed.html', {'tasks': tasks, 'editable': False , 'date': day})

        return render(request, 'completed.html', {'tasks': tasks, 'editable': False, 'date': day})

    return redirect('home')

def get_completed_by_date(request):
    if request.method == "GET":
        user = request.user
        date = request.GET.get('date')

        tasks = []
        if not date:
            return JsonResponse({'error': 'Date is required'}, status=400)
        if DayPlan.objects.filter(user=user, date=date).exists():
            plan = DayPlan.objects.get(user=user, date=date)
            tasks = Task.objects.filter(DayPlan=plan, is_completed=True)

            if date == str(date.today()):
                return render(request, 'completed.html', {'tasks': tasks, 'editable': True})
            else:
                return JsonResponse({'tasks': tasks, 'editable': False})
        
        return JsonResponse({'tasks': tasks, 'editable': False})



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
            return JsonResponse({'error': 'Date is required'}, status=400)
        
        if DayPlan.objects.filter(user=user, date=date).exists():
            plan = DayPlan.objects.get(user=user, date=date)
            tasks = Task.objects.filter(DayPlan=plan)

            task_data = []
            for task in tasks:
                task_data.append({
                    'name': task.task,
                    'hours': task.estimated_time.hour,
                    'minutes': task.estimated_time.minute,
                    'category': task.category,
                })
            
            return JsonResponse({'tasks': task_data})
        
        # Return an empty tasks list if no DayPlan exists for the date
        return JsonResponse({'tasks': []})
    
    # If the request method is not GET, return a 405 Method Not Allowed error
    return JsonResponse({'error': 'Invalid request method'}, status=405)
        
def update_completed(request):
    if request.method == 'POST':
        try:
            # Iterate over POST data to update tasks
            for key, value in request.POST.items():
                if key.startswith('is_completed_'):
                    # Extract task ID

                    print(key, value)
                    task_id = key.split('_')[2]
                    is_completed = value == 'true'



                    # Get remarks for this task
                    remarks_key = f'remarks_{task_id}'
                    remarks = request.POST.get(remarks_key, '').strip()

                    print(is_completed, remarks)

                    # Update the task in the database
                    Task.objects.filter(id=task_id).update(
                        is_completed=is_completed,
                        remarks=remarks
                    )

            messages.success(request, "Tasks updated successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        # Redirect back to the completed tasks page
        return redirect('/completed/')

    # If not a POST request, redirect to the tasks page
    return redirect('/completed/')
        

def get_progress(request):
    if request.method == 'GET':
        user = request.user
        today = date.today()

        if DayPlan.object.filter(user = user, date = today).exist():
            plan = DayPlan.objects.get(user = user, date = today)
            tasks = Task.objects.filter(DayPlan = plan)

            completed_time = (0, 0)
            total_time = (0, 0)
            

            for task in tasks:
                
                total_time= (total_time[0]+ task.estimated_time.hour, total_time[1] + task.estimated_time.minute) 

                if task.is_completed:
                    completed_time = (completed_time[0]+ task.estimated_time.hour, completed_time[1]+task.estimated_time.minute)

            progress = (completed_time[0]*60 +completed_time[1])/(total_time[0]*60 + total_time[1])*100

            response = JsonResponse({'progress': progress})
        else:
            response = JsonResponse({'progress': 0})

        return response