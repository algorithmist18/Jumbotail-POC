
# Import necessary modules

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def index(request): 

	return render(request, 'dashboard_page.html')