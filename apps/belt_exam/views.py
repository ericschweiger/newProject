from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def main(request):
    return render(request, 'belt_exam/login.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed)
        request.session['id'] = user.id
        return redirect('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        user = User.objects.get(username = request.POST['username'])
        request.session['id'] = user.id
        return redirect('/travels')

def trips(request):
    if 'id' not in request.session:
        messages.error(request, "Please login or register")
        return redirect('/main')
    else:
        user = User.objects.get(id=request.session['id'])
        trips = Trip.objects.all()
        my_trips = user.trips.all()
        other_trips = trips.difference(my_trips)

        context = {
            'user' : user,
            'my_trips' : my_trips,
            'other_trips' : other_trips
        }
        return render(request, 'belt_exam/trips.html', context)


def logout(request):
    request.session.clear()
    return redirect('/main')

def display_trip(request,trip_id):
    trip = Trip.objects.get(id = trip_id)
    user = User.objects.get(id = trip.creator.id)
    joiners = trip.trips.all().exclude(id = user.id)
    context = {
        'trip' : trip,
        'joiners' : joiners
    }
    return render(request, 'belt_exam/display.html', context)

def add_trip(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user' : user
    }
    return render(request, 'belt_exam/add_trip.html', context)

def create(request):
    user = User.objects.get(id=request.session['id'])
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
    else:
        trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], trip_start=request.POST['trip_start'], trip_end=request.POST['trip_end'], creator = user)
        user.trips.add(trip)
        return redirect('/travels')

def join(request, trip_id):
    user = User.objects.get(id = request.session['id'])
    trip = Trip.objects.get(id=trip_id)
    user.trips.add(trip)
    return redirect('/travels')

