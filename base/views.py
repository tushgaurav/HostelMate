from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Room, Comments, Type
from .forms import RoomForm
from django.contrib import messages


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist.")
    context = {}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(room_type__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )

    room_count = rooms.count()

    room_types = Type.objects.all()

    context = {"rooms": rooms, "types": room_types, "count": room_count}
    return render(request, 'home.html', context)

def room(request, pk):

    comments = Comments.objects.check()
    room = Room.objects.get(id=pk)
    context = {'room': room, 'comments': comments}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    context = {'form': form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def editRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You don't have the permissions to modify this room.")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, room_id):
    room = Room.objects.get(id=room_id)

    if request.user != room.host:
        return HttpResponse("You don't have the permissions to delete this room.")
    if request.method == 'POST':
        Room.delete(room)
        return redirect('home')
    
    context = {}
    return render(request, 'delete.html', context)