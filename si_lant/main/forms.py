from django import forms
from . import models
from django import forms
from .models import Service
from .models import Equipment, ServiceType, ServiceCompany  # Импортируем все используемые модели
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'equipment',        # Машина
            'service_company',  # Сервисная компания
            'Service_type',     # Вид ТО
            'Service_date',     # Дата проведения ТО
            'operating_time',   # Наработка, м/час
            'order',            # Номер заказ-наряда
            'order_date'        # Дата заказ-наряда
        ]

        # Настраиваем поля с выпадающими списками

    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        label="Машина"
    )
    service_company = forms.ModelChoiceField(
        queryset=ServiceCompany.objects.all(),
        label="Сервисная компания"
    )
    Service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        label="Вид ТО"
    )

    Service_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата проведения ТО"
    )

    order_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата заказ-наряда"
    )
class EquipmentSearchForm(forms.Form):
    vin = forms.CharField(max_length=10)


class EquipmentCreateForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'


class VehicleModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.VehicleModel
        fields = '__all__'


class EngineModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.EngineModel
        fields = '__all__'


class TransmissionModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.TransmissionModel
        fields = '__all__'


class DriveAxleModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.DriveAxleModel
        fields = '__all__'


class SteeringAxleModelCreateForm(forms.ModelForm):
    class Meta:
        model = models.SteeringAxleModel
        fields = '__all__'


class ServiceCompanyCreateForm(forms.ModelForm):
    class Meta:
        model = models.ServiceCompany
        fields = '__all__'


class ServiceTypeCreateForm(forms.ModelForm):
    class Meta:
        model = models.ServiceType
        fields = '__all__'


class DenialTypeCreateForm(forms.ModelForm):
    class Meta:
        model = models.DenialType
        fields = '__all__'


class RecoveryMethodCreateForm(forms.ModelForm):
    class Meta:
        model = models.RecoveryMethod
        fields = '__all__'


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'
        widgets = {
            'order': forms.Textarea(attrs={'rows': 1}),
            'Service_date': forms.NumberInput(attrs={'type': 'date'}),
            'order_date': forms.NumberInput(attrs={'type': 'date'}),
            'Equipment': forms.HiddenInput(),
            'service_company': forms.HiddenInput(),
        }


class ClaimCreateForm(forms.ModelForm):
    class Meta:
        model = models.Claim
        fields = '__all__'
        widgets = {
            'date_of_refusal': forms.NumberInput(attrs={'type': 'date'}),
            'failure_node': forms.Textarea(attrs={'rows': 1}),
            'parts_used': forms.Textarea(attrs={'rows': 1}),
            'date_of_restoration': forms.NumberInput(attrs={'type': 'date'}),
            'equipment_downtime': forms.Textarea(attrs={'rows': 1}),
            'equipment': forms.HiddenInput(),
            'service_company': forms.HiddenInput(),
        }


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'
        widgets = {
            'order': forms.Textarea(attrs={'rows': 1}),
            'Service_date': forms.NumberInput(attrs={'type': 'date'}),
            'order_date': forms.NumberInput(attrs={'type': 'date'}),
            'Equipment': forms.HiddenInput(),
            'service_company': forms.HiddenInput(),
        }
