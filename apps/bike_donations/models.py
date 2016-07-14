from __future__ import unicode_literals

from django.db import models
from ..bike_factors.models import *
from ..component_factors.models import *
# Create your models here.

class Bike(models.Model):
	bikeType = models.ForeignKey(BikeOption)
	brand = models.ForeignKey(BrandOption)
	cosmetic = models.ForeignKey(CosmeticOption)
	frame = models.ForeignKey(FrameOption, null=True, blank=True)
	features = models.ManyToManyField(FeaturesOption, blank=True)
	nego_factor = models.DecimalField(max_digits=3, decimal_places=2, default=1.05)
	price = models.DecimalField(max_digits=6, decimal_places=2, default=200.00)

class Component(models.Model):
	saddleSelect = models.ForeignKey(SaddleOption, null=True, blank=True)
	handleSelect = models.ForeignKey(HandlebarOption, null = True, blank=True)
	price = models.DecimalField(max_digits=6, decimal_places = 2)

