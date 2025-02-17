from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm, TaskForm, TaskStatusForm
from .models import Task

# Home View
def home(request):
    return render(request, 'testapp/home.html')

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            if user.is_manager:
                return redirect('manager_dashboard')
            elif user.is_employee:
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Error creating account. Please check the form.")
    else:
        form = SignUpForm()
    return render(request, 'testapp/signup.html', {'form': form})

# Manager Login View
def manager_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_manager:
            login(request, user)
            messages.success(request, "Logged in successfully as a manager!")
            return redirect('manager_dashboard')
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")
    return render(request, 'testapp/manager_login.html')

# Employee Login View
def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_employee:
            login(request, user)
            messages.success(request, "Logged in successfully as an employee!")
            return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")
    return render(request, 'testapp/employee_login.html')

# Manager Dashboard View
@login_required
def manager_dashboard(request):
    if not request.user.is_manager:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task assigned successfully!")
            return redirect('manager_dashboard')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(assigned_to__is_employee=True)
    return render(request, 'testapp/manager_dashboard.html', {'form': form, 'tasks': tasks})

# Assign Task View
@login_required
def assign_task(request):
    if not request.user.is_manager:
        messages.warning(request, "Only managers can assign tasks.")
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task assigned successfully!")
            return redirect('manager_dashboard')
    else:
        form = TaskForm()

    return render(request, 'testapp/assign_task.html', {'form': form})

# Employee Dashboard View
@login_required
def employee_dashboard(request):
    if not request.user.is_employee:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('manager_dashboard')

    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'testapp/employee_dashboard.html', {'tasks': tasks})

# Update Task Status View

@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.assigned_to != request.user:
        messages.error(request, "You are not authorized to update this task.")
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task status updated successfully!")
            return redirect('employee_dashboard')
    else:
        form = TaskStatusForm(instance=task)

    return render(request, 'testapp/update_task_status.html', {'form': form, 'task': task})