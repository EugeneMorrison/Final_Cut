"""
URL configuration for si_lant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views

# urlpatterns = [
#     path('account/', include('authentication.urls')),
#     path('', views.EquipmentListView.as_view(), name="index"),
#     path('user_index', views.AdminIndexListView.as_view(), name="user_index"),
#     path('Equipments/new', views.EquipmentCreateView.as_view(), name="Equipment-create"),
#     path('Equipments/<int:pk>', views.EquipmentDetailView.as_view(), name="Equipment-detail"),
#     path('Equipments/edit/<int:pk>', views.EquipmentUpdateView.as_view(), name="Equipment-update"),
#     path('Equipments/delete/<int:pk>', views.EquipmentDeleteView.as_view(), name="Equipment-delete"),

urlpatterns = [
    path('account/', include('authentication.urls')),
    path('', views.EquipmentListView.as_view(), name="index"),
    path('user_index/', views.EquipmentListView.as_view(), name="user_index"),

    path('Equipments/', views.AdminIndexListView.as_view(), name="equipment_list"),
    path('Equipments/new/', views.EquipmentCreateView.as_view(), name="equipment_create"),
    path('Equipments/<int:pk>/', views.EquipmentDetailView.as_view(), name="equipment_detail"),
    path('Equipments/<int:pk>/edit/', views.EquipmentUpdateView.as_view(), name="equipment_update"),
    path('Equipments/<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name="equipment_delete"),


    path('lookups', views.lookups, name="lookups"),

    path('lookups/vehicle_models', views.VehicleModelListView.as_view(), name="vehicle-model-list"),
    path('lookups/vehicle_models/new', views.VehicleModelCreateView.as_view(), name="vehicle-model-create"),
    path('lookups/vehicle_models/edit/<int:pk>', views.VehicleModelUpdateView.as_view(), name="vehicle-model-update"),

    path('lookups/engine_models', views.EngineModelListView.as_view(), name="engine-model-list"),
    path('lookups/engine_models/new', views.EngineModelCreateView.as_view(), name="engine-model-create"),
    path('lookups/engine_models/edit/<int:pk>', views.EngineModelUpdateView.as_view(), name="engine-model-update"),

    path('lookups/transmission_models', views.TransmissionModelListView.as_view(), name="transmission-model-list"),
    path('lookups/transmission_models/new', views.TransmissionModelCreateView.as_view(), name="transmission-model-create"),
    path('lookups/transmission_models/edit/<int:pk>', views.TransmissionModelUpdateView.as_view(), name="transmission-model-update"),

    path('lookups/drive_axles', views.DriveAxleListView.as_view(), name="drive-axle-list"),
    path('lookups/drive_axles/new', views.DriveAxleCreateView.as_view(), name="drive-axle-create"),
    path('lookups/drive_axles/edit/<int:pk>', views.DriveAxleUpdateView.as_view(), name="drive-axle-update"),

    path('lookups/steering_axles', views.SteeringAxleListView.as_view(), name="steering-axle-list"),
    path('lookups/steering_axles/new', views.SteeringAxleCreateView.as_view(), name="steering-axle-create"),
    path('lookups/steering_axles/edit/<int:pk>', views.SteeringAxleUpdateView.as_view(), name="steering-axle-update"),

    path('lookups/service_companies', views.ServiceCompanyListView.as_view(), name="service-company-list"),
    path('lookups/service_companies/new', views.ServiceCompanyCreateView.as_view(), name="service-company-create"),
    path('lookups/service_companies/edit/<int:pk>', views.ServiceCompanyUpdateView.as_view(), name="service-company-update"),

    path('lookups/Service_types', views.ServiceTypeListView.as_view(), name="Service-type-company-list"),
    path('lookups/Service_types/new', views.ServiceTypeCreateView.as_view(), name="Service-type-create"),
    path('lookups/Service_types/edit/<int:pk>', views.ServiceTypeUpdateView.as_view(), name="Service-type-update"),

    path('lookups/denial_types', views.DenialTypeListView.as_view(), name="denial-type-company-list"),
    path('lookups/denial_types/new', views.DenialTypeCreateView.as_view(), name="denial-type-create"),
    path('lookups/denial_types/edit/<int:pk>', views.DenialTypeUpdateView.as_view(), name="denial-type-update"),

    path('lookups/recovery_methods', views.RecoveryMethodListView.as_view(), name="recovery-method-company-list"),
    path('lookups/recovery_methods/new', views.RecoveryMethodCreateView.as_view(), name="recovery-method-create"),
    path('lookups/recovery_methods/edit/<int:pk>', views.RecoveryMethodUpdateView.as_view(), name="recovery-method-update"),

    path('Service', views.ServiceListView.as_view(), name="Service-list"),
    path('Service/new', views.ServiceCreateView.as_view(), name="Service-create"),
    path('Service/<int:pk>', views.ServiceDetailView.as_view(), name="Service-detail"),
    path('Service/edit/<int:pk>', views.ServiceUpdateView.as_view(), name="Service-update"),
    path('Service/delete/<int:pk>', views.ServiceDeleteView.as_view(), name="Service-delete"),

    path('Claims', views.ClaimListView.as_view(), name="Claim-list"),
    path('Claims/new', views.ClaimCreateView.as_view(), name="Claim-create"),
    path('Claims/<int:pk>', views.ClaimDetailView.as_view(), name="Claim-detail"),
    path('Claims/edit/<int:pk>', views.ClaimUpdateView.as_view(), name="Claim-edit"),
    path('Claims/delete/<int:pk>', views.ClaimDeleteView.as_view(), name="Claim-delete"),
]
