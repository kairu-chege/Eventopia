from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Event
from .forms import EventForm
from django.contrib.auth import authenticate, login
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages  # Import messages for error handling

def homepage(request):
    return render(request, 'events/homepage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #create a profile instance for the new user
            Profile.objects.create(user=user)
            login(request, user)  # Log in the user after successful signup
            print("Redirecting to profile....")
            return redirect('profile')  # Redirect to the event list or homepage
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, 'events/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to the profile page
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password.")
            return render(request, 'events/login.html', {'form': form})  # Use the existing form variable
    else:
        form = AuthenticationForm()  # Use Django's built-in AuthenticationForm
    return render(request, 'events/login.html', {'form': form})

def profile(request):
    user = request.user 
    profile = user.profile  # Access the associated Profile object
    context = {'profile': profile} 
    return render(request, 'events/profile.html', context)

# Event List View
def event_list(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'events/event_list.html', {'events': events})

# Event Detail View
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

# Event Create View
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')  # Redirect to the event list after saving
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

# Event Update View
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)  # Redirect to event details after update
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

# Event Delete View
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')  # Redirect to event list after deletion
    return render(request, 'events/event_confirm_delete.html', {'event': event})