# restaurantes/views.py

from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
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

def find_restaurant(request):
    return None

def edit_restaurant(request):
    cursor = list(restaurants.find())
    iterator = [(i, cursor[i]) for i in range(0, len(cursor))]

    paginator = Paginator(iterator, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    if page is None:
        page = 1

    restaurants_page = paginator.page(page)

    if request.method == "POST":
            form = RestaurantEditForm(request.POST)
            if form.is_valid():                   # se pasan los validadores
                data = form.cleaned_data

                print(restaurants.find({ restaurant_id: data["restaurant_id"] }))

                restaurants.findAndModify({
                    query: { restaurant_id: data["restaurant_id"] },
                    update: { name: data["name"] }
                })

                return redirect('/restaurantes/edit')
    else:
        form = RestaurantEditForm()

    context = {
        "range": range(0,len(iterator)),
        "restaurants": restaurants_page,
        "form": form,
    }
    return render(request, 'forms/edit_restaurant.html', context)

def create_restaurant(request):
    if request.method == "POST":
            form = RestaurantForm(request.POST)
            if form.is_valid():                   # se pasan los validadores
                data = form.cleaned_data
                print(data)
                restaurants.restaurants.insert_one(
                    {
                        "address": {
                            "street": data["street"],
                            "zipcode": data["zipcode"],
                            "building": data["building"],
                            "coord": [0,0]
                        },
                        "borough": data["borough"],
                        "cuisine": data["cuisine"],
                        "grades": [],
                        "name": data["name"],
                        "restaurant_id": ""
                    }
                )
                return redirect('/restaurantes/create')
    else:
        form = RestaurantForm()

    context = {
        "form": form,
    }
    return render(request, 'forms/create_restaurant.html', context)
