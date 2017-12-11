# restaurantes/views.py

from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .forms import *
from .models import restaurants

import json

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

def find_restaurant(request, type, data):
    if type == "cuisine":
        cursor = restaurants.find({"cuisine": data})
    elif type == "name":
        cursor = restaurants.find({"name": data})
    elif type == "borough":
        cursor = restaurants.find({"borough": data})
    elif type == "zip":
        cursor = restaurants.find({"address.zipcode": data})

    paginator = Paginator(cursor, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    if page is None:
        page = 1

    ret = []
    for doc in paginator.page(page):
        ret.append({"name": doc["name"], "cuisine": doc["cuisine"], "street": doc["address"]["street"], "number": doc["address"]["building"], "zip": doc["address"]["zipcode"], "borough": doc["borough"] })

    return HttpResponse(json.dumps(ret), content_type="application/json")

def find_restaurant_view(request):
    form = RestaurantFindForm()

    context = {
        "form": form,
    }
    return render(request, 'forms/find_restaurant.html', context)

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

                print(data)
                restaurants.update_one({ "restaurant_id": data["restaurant_id"] }, {'$set': { "name": data["name"] }}, upsert=True)

                return redirect('/restaurantes/edit')
    else:
        form = RestaurantEditForm()

    context = {
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
                restaurants.insert_one(
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
