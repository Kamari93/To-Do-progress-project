from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import VictoryForm
from .models import Victory
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'victory/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'victory/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('currentvictories')
            except IntegrityError:
                return render(request, 'victory/signupuser.html', {'form': UserCreationForm(), 'error': 'This username has already been taken. Please choose a new username.'})
        else:
            return render(request, 'victory/signupuser.html', {'form': UserCreationForm(), 'error':'Passwords do not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'victory/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'victory/loginuser.html', {'form': AuthenticationForm(), 'error': 'The username and password did not match'})
        else:
            login(request, user)
            return redirect('currentvictories')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createvictories(request):
    if request.method == 'GET':
        return render(request, 'victory/createvictories.html', {'form': VictoryForm()})
    else:
        try:
            form = VictoryForm(request.POST)
            newvictories = form.save(commit=False)
            newvictories.user = request.user
            newvictories.save()
            return redirect('currentvictories')
        except ValueError:
            return render(request, 'victory/createvictories.html', {'form': VictoryForm(), 'error':'Bad data passed in. Please try again!'})


@login_required
def currentvictories(request):
    victories = Victory.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'victory/currentvictories.html', {'victories':victories})

@login_required
def completedvictories(request):
    victories = Victory.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'victory/completedvictories.html', {'victories': victories})

@login_required
def viewvictory(request, victory_pk):
    victory = get_object_or_404(Victory, pk=victory_pk, user=request.user)
    if request.method == 'GET':
        form = VictoryForm(instance=victory)
        return render(request, 'victory/viewvictory.html', {'victory': victory, 'form': form})
    else:
        try:
            form = VictoryForm(request.POST, instance=victory)
            form.save()
            return redirect('currentvictories')
        except ValueError:
            return render(request, 'victory/viewvictory.html', {'victory': victory, 'form': form, 'error':'You can give me something better than that. Please try again!'})

@login_required
def completevictory(request, victory_pk):
    victory = get_object_or_404(Victory, pk=victory_pk, user=request.user)
    if request.method == 'POST':
        victory.datecompleted=timezone.now()
        victory.save()
        return redirect('currentvictories')

@login_required
def deletevictory(request, victory_pk):
    victory = get_object_or_404(Victory, pk=victory_pk, user=request.user)
    if request.method == 'POST':
        victory.delete()
        return redirect('currentvictories')
