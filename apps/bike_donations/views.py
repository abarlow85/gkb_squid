from django.shortcuts import render
from django.http import JsonResponse
from ..bike_factors.models import BikeOption, BrandOption, CosmeticOption, FeaturesOption, FrameOption, WheelOption
from .models import Bike
import requests
import json
from .api import LightspeedApi


# Create your views here.
def home(request):
	return render(request, 'bike_donations/index.html')

def form_data(request):
	context = {
		'bikeType' : serialize_selections(BikeOption.objects.all().values()),
		'wheels' : serialize_selections(WheelOption.objects.all().values()),
		'brand' : serialize_selections(BrandOption.objects.all().values()),
		'cosmetic' : serialize_selections(CosmeticOption.objects.all().values()),
		'frame' : serialize_selections(FrameOption.objects.all().values()),
		'features' : serialize_selections(FeaturesOption.objects.all().values())
	}
	return JsonResponse(context)


def serialize_selections(query_set):
	data = {}

	for obj in query_set:

		data[obj['option']] = {'status' : False, 'price_factor' : obj['price_factor']}

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

def sample_post(request):
	print ("IN the VIEWS ALL ALONE", request.body)
	parsed_json = json.loads(request.body)
	print ("parsed json", parsed_json)
	print("parsing for attributes", parsed_json['price'], parsed_json['bikeType'], parsed_json['cosmetic'], parsed_json['frame'])
	descriptionString = str(parsed_json['bikeType'] + " " + parsed_json['brand'] + " " + parsed_json['cosmetic'])
	bikePrice = parsed_json['price']
	print ("Stringify", descriptionString)

	# newBike = request.body
	lightspeed = LightspeedApi()

	newBicycle = lightspeed.create_bike(descriptionString, bikePrice)
	# print newBicycle
	return render(request, 'bike_donations/index.html')
