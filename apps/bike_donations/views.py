from django.shortcuts import render
from django.http import JsonResponse
from ..bike_factors.models import BikeOption, BrandOption, CosmeticOption, FeaturesOption, FrameOption, WheelOption
from .models import Bike, Component
from ..component_factors.models import HandlebarOption, SaddleOption
import requests
import json
import string
import random
from .api import LightspeedApi
from .forms import BikeForm, componentForm 
# from django.views.generic.base import TemplateView



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
	parsed_json = json.loads(request.body)
	optionsArray = []

	bikeoption = BikeOption.objects.get(option=parsed_json["bikeType"])
	optionsArray.append(bikeoption)

	brandoption = BrandOption.objects.get(option=parsed_json["brand"])
	optionsArray.append(brandoption)

	cosmeticoption = CosmeticOption.objects.get(option=parsed_json["cosmetic"])
	optionsArray.append(cosmeticoption)


	featuresoption = [FeaturesOption.objects.get(option=feature) for feature in parsed_json["features"]]

	if 'frame' in parsed_json:
		frameoption = FrameOption.objects.get(option=parsed_json["frame"])
		optionsArray.append(frameoption)
		parsed_json["frame"]=frameoption.id
	else:
		parsed_json['frame'] = None

	wheeloption = WheelOption.objects.get(option=parsed_json["wheels"])
	optionsArray.append(wheeloption)

	parsed_json["wheels"]=wheeloption.id
	parsed_json["features"]=[obj.id for obj in featuresoption]
	parsed_json["brand"]=brandoption.id
	parsed_json["cosmetic"]=cosmeticoption.id
	parsed_json["bikeType"] = bikeoption.id
	form = BikeForm(parsed_json)

	if form.is_valid():
		print ("In the forms", form["bikeType"].value())
		parsed_json["djangoPrice"] = getBikePrice(optionsArray, featuresoption)
	else:
		print ("Not valid", form.errors.as_json())
	descriptionString = str(bikeoption.option + " " + brandoption.option + " " + cosmeticoption.option)
	bikePrice = parsed_json['djangoPrice']
	lightspeed = LightspeedApi()

	#returns pythonDictionary
	newBicycle = lightspeed.create_item(descriptionString, bikePrice)

	# session for label template
	request.session['customSku'] = newBicycle['customSku']
	request.session['brand'] = brandoption.option
	request.session['bikeType'] = bikeoption.option
	request.session['price'] = bikePrice
	return JsonResponse({'success' : True})

def component_post(request):
	parsed_json = json.loads(request.body)
	optionsArray = []

	descriptionString = ""
	componentType = ""

	saddleSelect = None
	handleSelect = None 

	print 'made it to component post'
	if 'saddle' in parsed_json:
		saddleSelect = SaddleOption.objects.get(option=parsed_json['saddle'])
		print 'about to print saddleSelect'
		print saddleSelect
		optionsArray.append(saddleSelect)

		parsed_json['saddle'] = saddleSelect.id
		parsed_json['handlebar'] = None

		descriptionString = str(saddleSelect.option + " saddle")
		componentType = 'Saddle'

	elif 'handlebar' in parsed_json:
		handleSelect = HandlebarOption.objects.get(option=parsed_json['handlebar'])
		optionsArray.append(handleSelect)

		parsed_json['handlebar'] = handleSelect.id
		parsed_json['saddle'] = None

		descriptionString = str(handleSelect.option + " handlebar")
		componentType = 'Handlebar'

	form = componentForm(parsed_json)

	if form.is_valid():
		print ('we are valid')
	else:
		print ("Not valid", form.errors.as_json())

	lightspeed = LightspeedApi()

	#returns pythonDictionary
	newComponent= lightspeed.create_item(descriptionString, parsed_json['price'])

	# session for label template
	request.session['customSku'] = newComponent['customSku']
	if saddleSelect != None:
		request.session['brand'] = saddleSelect.option
	elif handleSelect != None:
		request.session['brand'] = handleSelect.option

	request.session['price'] = parsed_json['price']
	request.session['componentType'] = componentType
	return JsonResponse({'success' : True})


def getBikePrice(optionsArray, featuresoption):
	basePrice = 200.00
	price_factor = 1
	nego_factor = 1.05
	for option in optionsArray:
		print option, option.price_factor
		price_factor *= option.price_factor
	for feature in featuresoption:
		print feature, feature.price_factor
		price_factor *= feature.price_factor
	print ("price factor", price_factor, basePrice * float(price_factor) * nego_factor)
	return basePrice * float(price_factor) * nego_factor

def print_label(request):
	label = {
		'customSku' : request.session['customSku'],
		'brand' : request.session['brand'],
		'price' : request.session['price']
	}

	if 'bikeType' in request.session:
		label['type'] = request.session['bikeType']
	elif 'componentType' in request.session:
		label['type'] = request.session['componentType']

	return render(request, 'bike_donations/barcode.html', label)

def component_data(request):
	context = {
		'Handlebars' : serialize_componentFactor(HandlebarOption.objects.all()),
		'Saddles' : serialize_componentFactor(SaddleOption.objects.all()),
	}

	return JsonResponse(context)

def serialize_componentFactor(query_set):
	comp = {}

	for obj in query_set:
		comp[obj.option] = {'status': False, 'price': obj.price}

	print comp
	return comp







# def getBike(request):
# 	print (request.body)
# 	print request
# 	return render(request, 'bike_donations/confirmation.html')
