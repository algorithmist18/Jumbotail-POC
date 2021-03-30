"""jumbotail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard import views 

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.homepage, name = 'homepage'),
    path('assetIds', views.get_asset_IDs, name = 'get_asset_IDs'),
    path('validatetime', views.validate_times, name = 'validate_time'),
    path('fetchlocations', views.get_asset_locations, name = 'get_asset_locations'),
    path('position', views.save_position, name = 'save_position'),
    path('getnassets', views.get_n_assets, name = 'get_n_assets'),
    path('asset/<assetId>', views.get_asset_details, name = 'get_asset_details'),
    path('assetlocations', views.get_asset_locations_by_time_filter, name = 'get_asset_locations_by_time'),
    path('properties/<assetId>', views.get_asset_properties, name = 'get_asset_properties')

]
