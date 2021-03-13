
# Import necessary modules

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Position, Asset, Vehicle, Person
from .generate_test_data import generate_vehicles, generate_people, generate_positions

# Create your views here.

def index(request): 

	return render(request, 'dashboard_page.html')


def get_asset_location(request): 

	# Method to fetch list of positions for asset 

	# Generate testing data 

	vehicles = generate_vehicles(3) 
	people = generate_people(3) 
	positions = generate_positions(10) 

	# Handle requests 

	if request.method == 'POST': 

		# Fetch POST data 

		assetId = request.POST['assetId'] 
		startTime = request.POST['startTime']
		endTime = request.POST['endTime'] 

		# Query DB to fetch asset

		asset = Asset.objects.get(assetRegistrationId = assetId) 

		assetLocations = Position.objects.all().filter(asset = asset, time__lt = endTime, time__gt = startTime) 

		# Logging database elements to console 

		print(Vehicle.objects.all())
		print(Position.objects.all())
		print(Person.objects.all())

		# Return data 

		response = {'assetLocations' : assetLocations, 'assetId' : assetId} 

		return render(request, 'dashboard_page.html', response) 

	else: 

		print(Vehicle.objects.all())
		print(Position.objects.all())
		print(Person.objects.all())

		return render(request, 'dashboard_page.html') 