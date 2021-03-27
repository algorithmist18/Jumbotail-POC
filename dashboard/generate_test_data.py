# Importing libraries

import string, random, datetime
from .models import Asset, Person, Vehicle, Position, Trip, TripStop

# Global variables for names 

first_name = ['Raghav', 'Shanthini', 'Shiva', 'Venkat', 'Shailesh', 'Aditi', 'Ruhi', 'Akhilesh', 'Tejaswi', 'Thomas', 'Sanjay', 'Sohail', 'John', 'Annural']
last_name = ['Sachhar', 'Khan', 'Sundaram', 'Rathore', 'Gupta', 'Garg', 'Hariharan', 'Parekh', 'Yadav', 'Kumar', 'Karim', 'Gokhale']
vehicle_name = ['Ford F-150', 'Ford Ranger', 'Ram 1500', 'Nissan Frontier', 'GMC Canyon', 'Chevrolet Silverado 1500', 'Toyota Tundra']
companies = ['Tata Motors', 'Ashok Leyland', 'Eicher Motors', 'Nissan', 'Mahindra & Mahindra', 'Asia Motor Works']

# Generate testing data 

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