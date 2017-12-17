# restaurantes/views.py
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

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

@csrf_exempt
def find_restaurant(request, type):
    if type == "cuisine":
        data = request.POST.get('cuisine', '')
        print(data)
        cursor = restaurants.find({"cuisine": data})
    elif type == "name":
        data = request.POST.get('name', '')
        print(data)
        cursor = restaurants.find({"name": data})
    elif type == "borough":
        data = request.POST.get('borough', '')
        print(data)
        cursor = restaurants.find({"borough": data})
    elif type == "zip":
        data = request.POST.get('zip', '')
        print(data)

        cursor = restaurants.find({"address.zipcode": data})

    paginator = Paginator(cursor, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    if page is None:
        page = 1

    ret = []
    for doc in paginator.page(page):
        ret.append({"id": doc["restaurant_id"], "name": doc["name"], "cuisine": doc["cuisine"], "street": doc["address"]["street"], "number": doc["address"]["building"], "zip": doc["address"]["zipcode"], "borough": doc["borough"] })

    return HttpResponse(json.dumps(ret), content_type="application/json")

def find_restaurant_view(request):
    form = RestaurantFindForm()

    context = {
        "form": form,
    }
    return render(request, 'forms/find_restaurant.html', context)

def restaurant_detail_view(request, id):
    cursor = restaurants.find({"restaurant_id": id})
    final_doc = None

    for doc in cursor:
        final_doc = doc

    context = {
        "restaurant": final_doc,
    }
    return render(request, 'detail.html', context)

@login_required
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

@login_required
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

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'registration/complete_change_password.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

def stadistics(request):
    cursor = restaurants.find({}, {'cuisine': 1})
    total = cursor.count()
    types = {}

    for doc in cursor:
        if 'cuisine' in doc:
            if doc["cuisine"] not in list(types.keys()):
                types[doc["cuisine"]] = 1
            else:
                types[doc["cuisine"]] += 1

    return HttpResponse(json.dumps(types), content_type="application/json")


def stadistics_view(request):
    return render(request, 'stadistics.html')
