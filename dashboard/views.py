
# Import necessary modules

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Position, Asset, Vehicle, Person
from .generate_test_data import generate_vehicles, generate_people, generate_positions
import datetime 
from django.core import serializers 

# Create your views here.

def homepage(request): 

	# Generate new positions 

	# generate_positions(50) 

	return render(request, 'dashboard_page.html') 


def get_n_assets(request): 

	# Method to fetch list of positions for N assets

	if request.method == 'GET':

		response = {} 
		assets = [] 

		n = int(request.GET['noOfAssets']) 

		# Fetch data of 100 assets  

		assetList = list(Asset.objects.all().order_by('-time').values())

		for i in range(min(n, len(assetList))): 

			assets.append(assetList[i]) 

		response['assetsLocations'] = assets

	return JsonResponse(response) 


def get_asset_locations(request): 

	# Method to fetch the locations of asset 

	response = {} 

	if request.method == 'GET': 

		# Fetch POST data 

		assetId = request.GET['assetId'] 
		startTime = request.GET['startTime']
		endTime = request.GET['endTime'] 

		# Query DB to fetch asset

		assetLocations = Position.objects.all().filter(assetId = assetId).values()

		# Return data 

		response['assetLocations'] = list(assetLocations)

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

		startTime = datetime.datetime.strptime(request.GET['startTime'], "%Y-%m-%dT%H:%M")
		endTime = datetime.datetime.strptime(request.GET['endTime'], "%Y-%m-%dT%H:%M") 

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



def get_asset_locations_by_time_filter(request): 

	# Method to get all asset locations in between times 

	response = {} 

	if request.method == 'GET': 

		# Fetching data and converting to datetime 

		print(request.GET['startTime'])
		print(request.GET['endTime'])

		startTime = datetime.datetime.strptime(request.GET['startTime'], "%Y-%m-%dT%H:%M")
		endTime = datetime.datetime.strptime(request.GET['endTime'], "%Y-%m-%dT%H:%M") 

		# Logging into console 

		print(startTime, endTime)

		# Fetch all assets which fit the constraint 

		assets = list(Asset.objects.all().filter(time__gt = startTime, time__lt = endTime).order_by('-time').values()) 

		response['assets'] = assets 

		return JsonResponse(response) 

	else:

		return JsonResponse(response)  


