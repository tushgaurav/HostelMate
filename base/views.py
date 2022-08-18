from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Comments, Type
from .forms import RoomForm
from django.contrib import messages


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if (request.method == "POST"):
        username = request.POST.get('username').lower()
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
    context = {'page': 'login'}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration.")

    context = {'form': form}
    return render(request, 'login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(room_type__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )

    room_count = rooms.count()
    room_messages = Comments.objects.all()

    room_types = Type.objects.all()

    context = {
        "rooms": rooms,
        "types": room_types,
        "count": room_count,
        "room_messages": room_messages
          }
    return render(request, 'home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.comments_set.all().order_by('-created')
    occupants = room.occupants.all()

    if request.method == 'POST':
        message = request.POST.get('body')
        comment = Comments.objects.create(
            user=request.user,
            room = room,
            body = message
        )
        return redirect('room', pk=room.id)


    context = {'room': room, 'comments': comments, 'occupants': occupants}
    return render(request, 'room.html', context)

def userProfile(request, username):
    user = User.objects.get(username=username)
    rooms = user.room_set.all()
    comments = user.comments_set.all()
    context = {
        'user': user,
        'rooms': rooms,
        'comments': comments,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    context = {'form': form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
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


@login_required(login_url='login')
def deleteComment(request, comment_id):
    comment = Comments.objects.get(id=comment_id)

    if request.user != comment.user:
        return HttpResponse("You don't have the permissions to delete this room.")
    if request.method == 'POST':
        Comments.delete(comment)
        return redirect('home')
    
    context = {'object': comment}
    return render(request, 'delete.html', context)