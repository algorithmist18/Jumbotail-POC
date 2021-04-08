# Importing libraries

import string, random, datetime
from .models import Asset, Person, Vehicle, Position, Trip, TripStop
from django.contrib.auth.models import User

# Global variables for names 

first_name = ['Raghav', 'Shanthini', 'Shiva', 'Venkat', 'Shailesh', 'Aditi', 'Ruhi', 'Akhilesh', 'Tejaswi', 'Thomas', 'Sanjay', 'Sohail', 'John', 'Annural']
last_name = ['Sachhar', 'Khan', 'Sundaram', 'Rathore', 'Gupta', 'Garg', 'Hariharan', 'Parekh', 'Yadav', 'Kumar', 'Karim', 'Gokhale']
vehicle_name = ['Ford F-150', 'Ford Ranger', 'Ram 1500', 'Nissan Frontier', 'GMC Canyon', 'Chevrolet Silverado 1500', 'Toyota Tundra']
companies = ['Tata Motors', 'Ashok Leyland', 'Eicher Motors', 'Nissan', 'Mahindra & Mahindra', 'Asia Motor Works']

# Generate testing data 

def generate_admins(num = 5): 

	for i in range(num): 

		firstname = first_name[random.randint(0, len(first_name) - 1)]
		lastname = last_name[random.randint(0, len(last_name) - 1)]

		randomnumber = random.randint(10, 99) 
		username = firstname[:3].lower() + lastname[:3].lower() + str(len(firstname)) + str(randomnumber)
		email = username + '@gmail.com'
		password = 'root1234'

		print(email) 

		user = User(first_name = firstname, last_name = lastname, email = email, username = username, password = password) 
		user.save()


def generate_vehicles(num = 10):

	# Generate vehicles 

	vehicles = []

	for i in range(num): 

		name = vehicle_name[random.randint(0, len(vehicle_name) - 1)]
		company = companies[random.randint(0, len(companies) - 1)]

		vehicle = Vehicle(vehicleName = name, company = company) 
		asset = Asset(assetType = 'Truck', assetRegistrationId = vehicle.vehicleId) 

		# Save to database 

		vehicle.save() 
		asset.save() 

		print(vehicle) 

		vehicles.append(vehicle) 

	return vehicles 

def generate_people(num = 10): 

	# Generate people 

	people = [] 

	for i in range(num): 

		firstname = first_name[random.randint(0, len(first_name) - 1)]
		lastname = last_name[random.randint(0, len(last_name) - 1)]

		person = Person(name = firstname + ' ' + lastname) 
		person.save() 

		asset = Asset(assetType = 'Person', assetRegistrationId = person.personId) 

		# Save to database 

		asset.save() 

		print(person) 

		people.append(person) 

	return people 

def generate_positions(num = 100): 

	# Generate positions 

	noOfVehicles = len(Vehicle.objects.all())
	noOfPeople = len(Person.objects.all()) 

	positions = [] 

	for i in range(num): 

		# Generate truck and person alternately 

		if i % 2 == 0: 

			# Fetch a vehicle

			vehicle = Vehicle.objects.all()[random.randint(0, noOfVehicles - 1)]

			latitude = random.uniform(27.20, 27.22)
			longitude = random.uniform(77.49, 77.51)

			position = Position(assetId = vehicle.vehicleId, longitude = longitude, latitude = latitude) 
			position.save()

			# Update asset position 

			asset = Asset.objects.filter(assetRegistrationId = vehicle.vehicleId)[0]

		else: 

			# Fetch a person

			person = Person.objects.all()[random.randint(0, noOfPeople - 1)]

			latitude = random.uniform(27.20, 27.22)
			longitude = random.uniform(77.49, 77.51)

			position = Position(assetId = person.personId, longitude = longitude, latitude = latitude)
			position.save() 

			# Update asset position 

			asset = Asset.objects.get(assetRegistrationId = person.personId) 


		# Update latest location 

		asset.latitude = latitude
		asset.longitude = longitude
		asset.time = datetime.datetime.now() 

		asset.save() 

		positions.append(position) 

	return positions


def generate_trips(num): 

	noOfVehicles = len(Vehicle.objects.all())
	noOfPeople = len(Person.objects.all()) 

	positions = [] 

	for i in range(num): 

		# Generate truck and person alternately 

		if i % 2 == 0: 

			# Fetch a vehicle

			vehicle = Vehicle.objects.all()[random.randint(0, noOfVehicles - 1)]

			srcLat = random.uniform(27.20, 27.22)
			srcLon = random.uniform(77.49, 77.51)
			desLat = random.uniform(27.20, 27.22) 
			desLon = random.uniform(77.49, 77.51) 

			asset = Asset.objects.filter(assetRegistrationId = vehicle.vehicleId)[0]

			trip = Trip(srcLong = srcLon, srcLat = srcLat, desLat = desLat, desLong = desLon, asset = asset, startTime = datetime.datetime.now(), status = 'STARTED') 
			trip.save() 

			position = Position(assetId = vehicle.vehicleId, longitude = srcLon, latitude = srcLat)
			position.save() 

		else: 

			# Fetch a person

			person = Person.objects.all()[random.randint(0, noOfPeople - 1)]

			srcLat = random.uniform(27.20, 27.22)
			srcLon = random.uniform(77.49, 77.51)
			desLat = random.uniform(27.20, 27.22) 
			desLon = random.uniform(77.49, 77.51) 

			asset = Asset.objects.filter(assetRegistrationId = person.personId)[0]
			
			trip = Trip(srcLong = srcLon, srcLat = srcLat, desLat = desLat, desLong = desLon, asset = asset, startTime = datetime.datetime.now(), status = 'STARTED') 
			trip.save() 

			position = Position(assetId = person.personId, longitude = srcLon, latitude = srcLat)
			position.save() 

		# Update latest location 

		asset.latitude = srcLat
		asset.longitude = srcLon
		asset.time = datetime.datetime.now() 

		asset.save() 

def end_trips(): 

	trips = list(Trip.objects.filter(status = 'STARTED'))  

	for trip in trips: 

		trip.status = 'FINISHED'
		trip.endTime = datetime.datetime.now() 
		print(round((datetime.datetime.now() - trip.startTime).total_seconds(), 4))
		trip.time = round((datetime.datetime.now() - trip.startTime).total_seconds(), 4) 
		print(round((datetime.datetime.now() - trip.startTime).total_seconds(), 4))
		trip.save() 


def generate_trip_positions():

	trips = list(Trip.objects.all().filter(status = 'STARTED').values())

	for i in range(len(trips)): 

		asset = list(Asset.objects.filter(id = trips[i]['asset_id']).values())[0] 

		for i in range(4): 

			position = Position(assetId = asset['assetRegistrationId'], latitude = random.uniform(27.20, 27.22), longitude = random.uniform(77.49, 77.51)) 
			position.save() 



