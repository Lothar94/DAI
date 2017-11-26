# restaurantes/views.py

from django.shortcuts import render, HttpResponse

from .forms import RestaurantForm
from .models import restaurants

# Create your views here.

def index(request):
    iterator = restaurants.find().limit(20)
    context = {
        "restaurants": list(iterator)
    }
    return render(request, 'index.html', context)

def test_template(request):
    iterator = restaurants.find().limit(10)
    context = {
        "restaurants": list(iterator)
    }
    return render(request, 'test.html', context)

def edit_restaurant(request):
    if request.method == "POST":
            form = RestaurantForm(request.POST)
            if form.is_valid():                   # se pasan los validadores
                datos = form.cleaned_data
                return redirect('/restaurantes')
    else:
        form = RestaurantForm()

    context = {
        "form": form,
    }
    return render(request, 'forms/edit_restaurant.html', context)

def create_restaurant(request):
    if request.method == "POST":
            form = RestaurantForm(request.POST)
            if form.is_valid():                   # se pasan los validadores
                datos = form.cleaned_data
                return redirect('/restaurantes')
    else:
        form = RestaurantForm()

    context = {
        "form": form,
    }
    return render(request, 'forms/create_restaurant.html', context)
