# Importing libaries 

from django.utils.crypto import get_random_string
from datetime import datetime 
import string, random 

# ID Generator methods for Vehicle, Person and Trip

def generate_vehicle_ID(): 

	vehicleId = 'VEH' + get_random_string(7, allowed_chars = string.ascii_uppercase + string.digits)
	return vehicleId 

def generate_person_ID(): 

	personId = 'PER' + get_random_string(7, allowed_chars = string.ascii_uppercase + string.digits)
	return personId 

def generate_trip_ID(): 

	tripId = 'TRP' + get_random_string(12, allowed_chars = string.ascii_uppercase + string.digits) 
	return tripId

def generate_stop_ID(): 

	stopId = 'STP' + get_random_string(12, allowed_chars = string.ascii_uppercase + string.digits) 
	return stopId 

def generate_default_asset_ID(): 

	assetId = 'ANON' + get_random_string(6, allowed_chars = string.ascii_uppercase + string.digits) 
	return assetId

def generate_default_trip_ID(): 

	tripId = 'DEFTRP' + get_random_string(9, allowed_chars = string.ascii_uppercase + string.digits)
	return tripId

