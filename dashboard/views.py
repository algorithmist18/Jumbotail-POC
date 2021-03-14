
# Import necessary modules

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Position, Asset, Vehicle, Person
from .generate_test_data import generate_vehicles, generate_people, generate_positions
import datetime 
from django.core import serializers 

# Create your views here.

def homepage(request): 

	# Method to fetch list of positions for asset

	return render(request, 'dashboard_page.html')


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