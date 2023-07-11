from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, AccountCreation, EditAccount
from django.contrib.auth.models import auth
from django.contrib import messages as mg
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_messages = Message.objects.all()

    context = {'rooms': rooms, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'index.html', context)


@login_required(login_url='login')
def roomCrateion(request):
    topic = Topic.objects.all()
    form = RoomForm()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            name=request.POST.get('name'),
            topic=topic,
            description=request.POST.get('description')
        )

        return redirect('home')

    context = {'topics': topic, 'form': form}
    return render(request, 'create-room.html', context)


@login_required(login_url='login')
def room(request, pk):
    rooms = Room.objects.get(id=pk)
    room_messages = rooms.message_set.all()
    participants = rooms.participants.all()


    if request.method == 'POST':
        Message.objects.create(
            user = request.user,
            room = rooms,
            body = request.POST.get('body')
        )
        # mgs.save()
        rooms.participants.add(request.user)
        return redirect('room', pk=rooms.id)

    context = {'room': rooms, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'room.html', context)


@login_required(login_url='login')
def editRoom(request, pk):
    edit = True
    room = Room.objects.get(id=pk)
    topic = room.topic.name

    form = RoomForm(instance=room)

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')

        room.save()

        return redirect('room', pk=room.id)

    return render(request, 'create-room.html', {'form': form, 'edit': edit, 'topic': topic})

@login_required(login_url='login')
def deleteMessage(request, pk):
    obj = Message.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': obj})

@login_required(login_url='login')
def deleteRoomMessage(request, pk):
    obj = Message.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('room', pk=obj.room.id)
    return render(request, 'delete.html', {'obj': obj})


@login_required(login_url='login')
def deleteRoom(request, pk):
    obj = Room.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': obj})

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    rooms = user.room_set.all()

    context = {'topics': topics, 'rooms': rooms, 'room_messages': room_messages, 'user': user}
    return render(request, 'profile.html', context)


def topics(request):
    topics = Topic.objects.all()
    return render(request, 'topics.html', {'topics': topics})

@login_required(login_url='login')
def editProfile(request, pk):
    user = User.objects.get(id=pk)
    form = EditAccount(instance=user)

    if request.method == 'POST':
        form = EditAccount(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'edit-user.html', {'form':form})








def registerUser(request):
    form = AccountCreation()

    if request.method == 'POST':
        form = AccountCreation(request.POST)

        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            # user.save()
            return redirect('home')
        else:
            mg.error(request, 'Registration Not Successful')

    context = {'form': form}
    return render(request, 'signup.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(email=username, password=password)

        if user != None:
            auth.login(request, user)
            return redirect('home')

        else:
            mg.error(request, 'Invalid Username or Password')
    return render(request, 'login.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('home')
