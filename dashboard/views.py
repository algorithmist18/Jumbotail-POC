
# Import necessary modules

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Position, Asset, Vehicle, Person
from .generate_test_data import generate_vehicles, generate_people, generate_positions
#import datetime 
from django.core import serializers 
from datetime import datetime,timedelta  #Use this instead of import datetime
from django.db import connection 
import json 
from django.core.serializers import serialize
from math import sin, cos, asin, radians, sqrt

# Create your views here.

def homepage(request): 

	# Generate new positions

	"""
	generate_vehicles(10)
	generate_people(10)
	generate_positions(100)
	""" 

	generate_positions(10) 

	return render(request, 'dashboard_page.html')


def get_n_assets(request): 

	# Method to fetch list of positions for N assets

	assetMapping = {} 

	if request.method == 'GET':

		response = {} 
		assets = [] 

		n = int(request.GET['noOfAssets']) 

		# Fetch data of 100 assets  

		assetList = list(Asset.objects.all().order_by('-time').values())

		now = datetime.now()

		for i in range(min(n, len(assetList))): 

			
			#we dont want the data displayed on map to be too old
			if ( now-timedelta(hours=168) <= assetList[i]['time'] <= now ):  #currently set to 1 week i.e 168hrs
				
				if assetList[i]['assetRegistrationId'].startswith('PER'): 

					person = list(Person.objects.filter(personId = assetList[i]['assetRegistrationId']).values())
					assetMapping[assetList[i]['assetRegistrationId']] = person[0]

				else: 

					vehicle = list(Vehicle.objects.filter(vehicleId = assetList[i]['assetRegistrationId']).values())
					print(vehicle) 
					assetMapping[assetList[i]['assetRegistrationId']] = vehicle[0]

				assets.append(assetList[i]) 

			else: 

				break 

		response['assetsLocations'] = assets
		response['assetMap'] = assetMapping 

	return JsonResponse(response) 


def get_asset_locations(request): 

	# Method to fetch the locations of asset 

	response = {} 
	assetMapping = {} 

	if request.method == 'GET': 

		# Fetch POST data 

		assetId = request.GET['assetId'] 
		startTime = request.GET['startTime']
		endTime = request.GET['endTime'] 

		# Query DB to fetch asset

		assetLocations = Position.objects.all().filter(assetId = assetId, time__range = [startTime, endTime]).values()

		if assetId.startswith('PER'): 

			person = list(Person.objects.filter(personId = assetId).values())
			assetMapping[assetId] = person[0]

		else: 

			vehicle = list(Vehicle.objects.filter(vehicleId = assetId).values()) 
			assetMapping[assetId] = vehicle[0]
		
		# Return data 

		response['assetLocations'] = list(assetLocations)
		response['assetMapping'] = assetMapping 

		return JsonResponse(response) 

	else:

		return JsonResponse(response) 


def get_asset_IDs(request): 

	# Method to fetch all the trucks 

	response = {} 

	if request.method == 'GET': 

		assetIds = []

		if request.GET['assetType'] == 'Truck': 

			# Fetch the vehicles (trucks, in this case) 

			vehicles = Vehicle.objects.all() 

			for vehicle in vehicles: 

				assetIds.append(vehicle.vehicleId) 
		else:

			# Fetch the people  

			people = Person.objects.all() 

			for person in people: 

				assetIds.append(person.personId) 

		response['assetIds'] = assetIds 

		return JsonResponse(response)

	else: 

		return JsonResponse(response) 


def validate_times(request): 

	# Method to validate start time and end time 

	response = {} 

	if request.method == 'GET': 

		# Fetching data and converting to datetime 

		startTime = datetime.strptime(request.GET['startTime'], "%Y-%m-%dT%H:%M")
		endTime = datetime.strptime(request.GET['endTime'], "%Y-%m-%dT%H:%M") 

		# Logging into console 

		print(startTime, endTime)

		# Compare dates 

		if endTime < startTime: 

			response['valid'] = 'NO'
			response['message'] = 'End time cannot be before start time' 

		else:

			response['valid'] = 'YES'
			response['message'] = 'Valid time' 

		return JsonResponse(response) 

	else: 

		return JsonResponse(response) 


def save_position(request): 

	# Method to save position data 

	response = {} 

	if request.method == 'POST': 

		# Fetch request data

		assetId = request.POST['assetId']
		latitude = request.POST['latitude']
		longitude = request.POST['longitude'] 
		time = datetime.now() 

		# Check if valid data 

		if Asset.objects.filter(assetRegistrationId = assetId).exists() == False: 

			# Not a valid request 

			response['valid'] = False
			response['statusCode'] = 501

			return JsonResponse(response) 

		else: 

			# Save to Position database 

			position = Position(latitude = latitude, longitude = longitude, assetId = assetId, time = time)  
			position.save() 

			# Update Asset table 

			asset = Asset.objects.get(assetRegistrationId = assetId) 

			asset.latitude = latitude 
			asset.longitude = longitude
			asset.time = time

			asset.save()

			# Update response and return 

			response['valid'] = True
			response['positionId'] = position.id 
			response['message'] = 'Position saved successfully' 
			response['statusCode'] = 201 

			return JsonResponse(response)

	else: 

		response['statusCode'] = 403
		return JsonResponse(response) 


def get_asset_details(request, assetId): 

	# Method to get details of an asset 

	response = {}

	if request.method == 'GET': 

		print('Inside get_asset_details()') 

		try: 

			asset = list(Asset.objects.all().filter(assetRegistrationId = assetId).values())

			response['valid'] = True
			response['asset'] = asset

		except Asset.DoesNotExist:

			# Invalid asset ID 

			print('Invalid assetID, asset not found')
			response['valid'] = False


		return JsonResponse(response) 

	else: 

		return JsonResponse(response) 


def get_asset_properties(request, assetId): 

	# Method to get details of an asset 

	response = {}

	if request.method == 'GET': 

		print('Inside get_asset_properties()') 

		try: 

			asset = Asset.objects.get(assetRegistrationId = assetId)

			print(asset)

			if asset.assetType == "Vehicle": 

				vehicle = list(Vehicle.objects.all().filter(vehicleId = assetId).values())
				response['asset'] = vehicle

			else:

				person = list(Person.objects.all().filter(personId = assetId).values())
				response['asset'] = person 

			response['valid'] = True

		except Asset.DoesNotExist:

			# Invalid asset ID 

			print('Invalid assetID, asset not found')
			response['valid'] = False


		return JsonResponse(response) 

	else: 

		return JsonResponse(response) 


def get_asset_locations_by_time_filter(request): 

	# Method to get all asset locations in between times 

	response = {} 
	assetMapping = {} 

	if request.method == 'GET': 

		# Fetching data and converting to datetime 

		print(request.GET['startTime'])
		print(request.GET['endTime'])

		startTime = datetime.strptime(request.GET['startTime'], "%Y-%m-%dT%H:%M")
		endTime = datetime.strptime(request.GET['endTime'], "%Y-%m-%dT%H:%M") 

		# Logging into console 

		print(startTime, endTime)

		# Fetch all assets which fit the constraint 

		assets = list(Asset.objects.all().filter(time__gt = startTime, time__lt = endTime).order_by('-time').values()) 

		for i in range(len(assets)): 

			if assets[i]['assetRegistrationId'].startswith('PER'): 

				person = list(Person.objects.filter(personId = assets[i]['assetRegistrationId']).values())
				assetMapping[assets[i]['assetRegistrationId']] = person[0]

			else: 

				vehicle = list(Vehicle.objects.filter(vehicleId = assets[i]['assetRegistrationId']).values()) 
				assetMapping[assets[i]['assetRegistrationId']] = vehicle[0]

		# Update response 

		response['assetLocations'] = assets 
		response['assetMapping'] = assetMapping 

		return JsonResponse(response) 

	else:

		return JsonResponse(response)  



def validate_asset_ID(assetId): 

	# Method to check whether asset ID is valid or not 

	if assetId.startswith('PER') == True: 

		if not Person.objects.get(personId = assetId).exists(): 

			return False 

		return True 

	else: 

		if not Vehicle.objects.get(assetId = assetId).exists(): 

			return False 

		return True 


def start_trip(request): 

	# Method to start a trip 

	response = {} 

	if request.method == 'POST': 

		# Fetch request data 

		srcLong = request.POST['srcLong'] 
		srcLat = request.POST['srcLat']

		desLong = request.POST['desLong']
		desLat = request.POST['desLat']

		time = request.POST['time']

		assetId = request.POST['assetId'] 

		# Create new trip 

		if validate_asset_ID(assetId): 

			# Valid request 

			asset = Asset.objects.get(assetRegistrationId = assetId) 

			trip = Trip(asset = asset, status = 'STARTED', srcLong = srcLong, srcLat = srcLat, desLong = desLong, desLat = desLat, time = time) 

			trip.save() 

			response['valid'] = True 
			response['tripId'] = trip.tripId 

			return JsonResponse(response) 

		else: 

			response['valid'] = False 
			return JsonResponse(response) 

	else: 

		return JsonResponse(response) 


def compare_location(lon1, lat1, lon2, lat2): 

	# Method to compare how much distance is between these locations using haversine formula 

	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) 

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon2/2) ** 2
	c = 2 * asin(sqrt(a)) 
	r = 6371.8

	return c * r 


def end_trip(request): 

	# Method to end a trip 

	response = {} 
	delta = 0.50

	if request.method == 'POST': 

		# Fetch request data 

		locationLon = request.POST['locationLon']
		locationLat = request.POST['locationLat'] 
		tripId = request.POST['tripId']
		time = request.POST['time'] 

		# Check if trip is valid 

		trip = Trip.objects.get(tripId = tripId) 

		if compare_location(locationLon, locationLat, trip.desLon, trip.desLat) <= delta:

			# Acceptable 

			trip.status = 'FINISHED'

			# Compute time difference and edit 

			trip.save() 

			# Populate response 

			response['statusCode'] = 200
			response['valid'] = True
			response['tripId'] = tripId 

			return JsonResponse(response) 

		else:

			# Unacceptable 

			response['statusCode'] = 403
			response['valid'] = False 
			return JsonResponse(response) 

	else: 

		response['statusCode'] = 405
		return JsonResponse(response) 