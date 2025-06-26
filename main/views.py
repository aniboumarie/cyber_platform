from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib import messages
from .form import LessonForm, UserGroupForm, UserCreationForm

# Home view
def home(request):
    return render(request, 'home.html')


# Signup view with role assignment
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid() and role in ['Admin', 'Trainer', 'Trainee']:
            user = form.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')


# Dashboard view
@login_required
def dashboard_view(request):
    if request.user.groups.filter(name='Admin').exists():
        role = 'Admin'
    elif request.user.groups.filter(name='Trainer').exists():
        role = 'Trainer'
    elif request.user.groups.filter(name='Trainee').exists():
        role = 'Trainee'
    else:
        role = 'Unassigned'
    return render(request, 'dashboard.html', {'role': role})


# Lesson add view
def is_trainer(user):
    return user.groups.filter(name='Trainer').exists()


@login_required
@user_passes_test(is_trainer)
def add_lesson_view(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = LessonForm()
    return render(request, 'add_lesson.html', {'form': form})


# Role-checking decorator
def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)


# Remove duplicate/obsolete role-based dashboard views and keep only the new, secure versions

def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

from django.contrib.auth.views import LoginView
from django.urls import reverse

class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return reverse('admin_dashboard')
        elif user.groups.filter(name='Trainer').exists():
            return reverse('trainer_dashboard')
        elif user.groups.filter(name='Trainee').exists():
            return reverse('trainee_dashboard')
        else:
            return reverse('unauthorized')

@login_required
def admin_dashboard(request):
    print("Admin dashboard view called")  # This shows in terminal
    if not user_in_group(request.user, 'Admin'):
        return redirect('unauthorized')
    return render(request, 'dashboard/admin_dashboard.html')

@login_required
def trainer_dashboard(request):
    if not user_in_group(request.user, 'Trainer'):
        return redirect('unauthorized')
    return render(request, 'dashboard/trainer_dashboard.html')

@login_required
def trainee_dashboard(request):
    if not user_in_group(request.user, 'Trainee'):
        return redirect('unauthorized')
    return render(request, 'dashboard/trainee_dashboard.html')

# Optional: a simple unauthorized page
def unauthorized(request):
    return render(request, 'unauthorized.html')


@login_required
def manage_users(request):
    # Only allow Admins
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('unauthorized')

    users = User.objects.all()
    forms = []

    for user in users:
        initial_group = user.groups.first()  # Get first group if exists
        form = UserGroupForm(initial={'group': initial_group}, instance=user, prefix=user.username)
        forms.append((user, form))

    if request.method == 'POST':
        for user in users:
            form = UserGroupForm(request.POST, instance=user, prefix=user.username)
            if form.is_valid():
                # Remove user from all groups first
                user.groups.clear()
                # Then add the selected group
                selected_group = form.cleaned_data['group']
                user.groups.add(selected_group)
        return redirect('manage_users')

    return render(request, 'manage_users.html', {'forms': forms})

@login_required
def create_user(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('unauthorized')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('manage_users')
    else:
        form = UserCreationForm()

    return render(request, 'create_user.html', {'form': form})

@login_required
def some_view(request):
    # your logic here (e.g., saving data, logging in, etc.)
    messages.success(request, "User role updated successfully!")
    return redirect('some-page')  # or render(...)

# Course Detail Page Views
def network_security_view(request):
    return render(request, 'courses/network_security.html')

def ethical_hacking_view(request):
    return render(request, 'courses/ethical_hacking.html')

def cloud_security_view(request):
    return render(request, 'courses/cloud_security.html')

def incident_response_view(request):
    return render(request, 'courses/incident_response.html')
