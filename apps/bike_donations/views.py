from django.shortcuts import render
from django.http import JsonResponse
from ..bike_factors.models import BikeOption, BrandOption, CosmeticOption, FeaturesOption, FrameOption, WheelOption
from .models import Bike
import requests
from .api import LightspeedApi


# Create your views here.
def home(request):
	return render(request, 'bike_donations/index.html')

def form_data(request):
	context = {
		'bikeType' : serialize_selections(BikeOption.objects.all()),
		'wheels' : serialize_selections(WheelOption.objects.all()),
		'brand' : serialize_selections(BrandOption.objects.all()),
		'cosmetic' : serialize_selections(CosmeticOption.objects.all()),
		'frame' : serialize_selections(FrameOption.objects.all()),
		'features' : serialize_selections(FeaturesOption.objects.all())
	}
	return JsonResponse(context)


def serialize_selections(query_set):
	data = {}

	for obj in query_set:
		if type(obj) == BikeOption:
			data[obj.option] = {'status' : False, 'price_factor' : obj.price_factor}
		else:
			requisites = []
			for req in obj.requisites.values():
				requisites.append(req['option'])
				

			data[obj.option] = {'status' : False, 'price_factor' : obj.price_factor, 'requisites':requisites}
	print data

	return data

def get_inv(request):
	lightspeed = LightspeedApi()
	inventory = lightspeed.get_inventory()
	print inventory
	return JsonResponse(inventory, safe=False)

def create_category(request):
	print ("IN the views with AMERICA", request)

	lightspeed = LightspeedApi()
	category = lightspeed.create_category()
	
	print category 
	return render(request, 'bike_donations/index.html')
