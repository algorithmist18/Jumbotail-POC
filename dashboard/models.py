# Importing libraries 

from django.db import models
from .utils import generate_vehicle_ID, generate_person_ID, generate_trip_ID, generate_stop_ID, generate_default_asset_ID, generate_default_trip_ID

# Create your models here.

class Asset(models.Model): 

	# Table for storing the type of assets currently used (trucks, salespersons, etc.) 

	assetType = models.TextField(null = False) 
	assetRegistrationId = models.CharField(null = False, max_length = 10) 


class Vehicle(models.Model): 

	# Table for storing vehicle details 

	vehicleName = models.TextField(null = False) 
	vehicleId = models.CharField(null = False, default = generate_vehicle_ID, primary_key = True, max_length = 10) 
	company = models.TextField(null = False) 


class Person(models.Model): 

	# Table for storing person details 

	personId = models.CharField(null = False, default = generate_person_ID, primary_key = True, max_length = 10) 
	name = models.TextField(null = False) 
	phone = models.CharField(blank = True, max_length = 10) 
	email = models.TextField(blank = True) 
	address = models.TextField(blank = True) 


class Trip(models.Model): 

	# Table for storing trip details

	tripId = models.CharField(null = False, default = generate_trip_ID, primary_key = True, max_length = 12) 

	asset = models.ForeignKey(Asset, null = False, default = generate_default_asset_ID, on_delete = models.SET_DEFAULT)  

	# Source details 

	srcLong = models.DecimalField(null = False, max_digits = 19, decimal_places = 16)  
	srcLat = models.DecimalField(null = False, max_digits = 19, decimal_places = 16) 
	
	# Destination details 

	desLong = models.DecimalField(null = False, max_digits = 19, decimal_places = 16) 
	desLat = models.DecimalField(null = False, max_digits = 19, decimal_places = 16)

	# Time taken in minutes 

	time = models.DecimalField(null = False, max_digits = 8, decimal_places = 4) 


class TripStop(models.Model): 

	# Table for storing trip stops details 

	stopId = models.CharField(null = False, default = generate_stop_ID, primary_key = True, max_length = 12) 
	trip = models.ForeignKey(Trip, null = False, default = generate_default_trip_ID, on_delete = models.SET_DEFAULT)
	
	# Location details 

	locationLat = models.DecimalField(null = False, max_digits = 19, decimal_places = 16)
	locationLon = models.DecimalField(null = False, max_digits = 19, decimal_places = 16)

	# Order of stop in the trip 

	order = models.IntegerField(null = False) 


class Position(models.Model): 

	# Table for storing GPS request data

	assetId = models.CharField(null = False, default = generate_default_asset_ID, max_length = 10) 

	# Location data 

	longitude = models.DecimalField(null = False, max_digits = 19, decimal_places = 16) 
	latitude = models.DecimalField(null = False, max_digits = 19, decimal_places = 16) 

	# Using auto_now_add = True for storing the time when the object is created

	time = models.DateTimeField(auto_now_add = True) 
