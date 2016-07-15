from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import View
from .forms import CustomSkuForm
from ..bike_donations.api import LightspeedApi


# Create your views here.

class Home(View):
	form = CustomSkuForm()

	def get(self, request):
		return render(request, 'get_inventory/index.html', {'form' : self.form})

class Search(View):

	def get(self, request, sku):
		print sku
		form = CustomSkuForm({'customSku': sku})

		if form.is_valid():
			api = LightspeedApi()
			item = api.get_item(form.cleaned_data['customSku'])
			print item
			return JsonResponse(item, safe=False)
		else:
			return render(request, 'get_inventory/index.html', {'form':form})

@csrf_exempt
def delete_item(request):

	api = LightspeedApi()
	confirm = api.delete_item(request.body)
	return JsonResponse({'status':True})


