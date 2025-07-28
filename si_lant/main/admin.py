from django.contrib import admin
from . import models

# @admin.register(models.Equipment)
# class EquipmentAdmin(admin.ModelAdmin):
#     list_display = ('vin', 'vehicle_model', 'engine_model', 'transmission_model', 'user')
#     search_fields = ('vin',)
#     autocomplete_fields = ('vehicle_model', 'engine_model', 'transmission_model', 'drive_axle', 'steering_axle', 'service_company', 'user')

admin.site.register(models.Equipment)
admin.site.register(models.Claim)
admin.site.register(models.DriveAxleModel)
admin.site.register(models.EngineModel)
admin.site.register(models.FailureNode)
admin.site.register(models.Service)
admin.site.register(models.ServiceType)
admin.site.register(models.RecoveryMethod)
admin.site.register(models.ServiceCompany)
admin.site.register(models.SteeringAxleModel)
admin.site.register(models.TransmissionModel)
admin.site.register(models.VehicleModel)
admin.site.register(models.DenialType)