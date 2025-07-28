from typing import Any
from django.shortcuts import render
from . import models, forms
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from authentication import models as auth_models
from django.db.models import Q
from .models import Equipment, VehicleModel, EngineModel, TransmissionModel, DriveAxleModel, SteeringAxleModel, ServiceCompany
from authentication.models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServiceForm

def service_create(request):
    equipments = Equipment.objects.all()
    service_types = Service_type.objects.all()
    service_companies = ServiceCompany.objects.all()  # добавляем

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')  # куда у тебя редирект
    else:
        form = ServiceForm()

    return render(request, 'service_new.html', {
        'form': form,
        'Equipments': equipments,
        'Service_types': service_types,
        'service_companies': service_companies  # передаем в шаблон
    })



def new_service(request):
    equipments = Equipment.objects.all()
    service_companies = ServiceCompany.objects.all()
    organizations = Organization.objects.all()
    service_types = ServiceType.objects.all()

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()

    return render(request, 'service_new.html', {
        'Equipments': equipments,
        'service_companies': service_companies,
        'organizations': organizations,
        'Service_types': service_types,
        'form': form
    })

def index(request):
    return render(request, 'main/index.html')

class UserIndexListView(ListView):
    model = Equipment
    template_name = "user_index.html"
    context_object_name = "Equipments"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметры фильтрации из GET
        vin = self.request.GET.get('vin', '')
        vehicle_model = self.request.GET.get('vehicle_model', '')
        engine_model = self.request.GET.get('engine_model', '')
        engine_number = self.request.GET.get('engine_number', '')
        transmission_model = self.request.GET.get('transmission_model', '')
        transmission_number = self.request.GET.get('transmission_number', '')
        drive_axle = self.request.GET.get('drive_axle', '')
        drive_axle_number = self.request.GET.get('drive_axle_number', '')
        steering_axle = self.request.GET.get('steering_axle', '')
        steering_axle_number = self.request.GET.get('steering_axle_number', '')
        supply_agreement = self.request.GET.get('supply_agreement', '')
        shipment_date = self.request.GET.get('shipment_date', '')
        consignee = self.request.GET.get('consignee', '')
        delivery_address = self.request.GET.get('delivery_address', '')
        equipment_filter = self.request.GET.get('equipment', '')
        user_filter = self.request.GET.get('user', '')
        service_company = self.request.GET.get('service_company', '')

        # Применяем фильтры
        if vin:
            queryset = queryset.filter(vin__icontains=vin)
        if vehicle_model:
            queryset = queryset.filter(vehicle_model__name__icontains=vehicle_model)
        if engine_model:
            queryset = queryset.filter(engine_model__name__icontains=engine_model)
        if engine_number:
            queryset = queryset.filter(engine_number__icontains=engine_number)
        if transmission_model:
            queryset = queryset.filter(transmission_model__name__icontains=transmission_model)
        if transmission_number:
            queryset = queryset.filter(transmission_number__icontains=transmission_number)
        if drive_axle:
            queryset = queryset.filter(drive_axle__name__icontains=drive_axle)
        if drive_axle_number:
            queryset = queryset.filter(drive_axle_number__icontains=drive_axle_number)
        if steering_axle:
            queryset = queryset.filter(steering_axle__name__icontains=steering_axle)
        if steering_axle_number:
            queryset = queryset.filter(steering_axle_number__icontains=steering_axle_number)
        if supply_agreement:
            queryset = queryset.filter(supply_agreement__icontains=supply_agreement)
        if shipment_date:
            queryset = queryset.filter(shipment_date=shipment_date)
        if consignee:
            queryset = queryset.filter(consignee__icontains=consignee)
        if delivery_address:
            queryset = queryset.filter(delivery_address__icontains=delivery_address)
        if equipment_filter:
            queryset = queryset.filter(equipment__icontains=equipment_filter)
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)
        if service_company:
            queryset = queryset.filter(service_company__name__icontains=service_company)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Справочники для селектов
        context.update({
            "vehicle_model": VehicleModel.objects.all(),
            "engine_model": EngineModel.objects.all(),
            "transmission_model": TransmissionModel.objects.all(),
            "drive_axle": DriveAxleModel.objects.all(),
            "steering_axle": SteeringAxleModel.objects.all(),
            "clients": CustomUser.objects.filter(groups__name='customer'),
            "service_companies": ServiceCompany.objects.all()
        })
        return context

class EquipmentListView(FormMixin, ListView):
    model = models.Equipment
    template_name = 'main/index.html'
    context_object_name = 'Equipments'
    form_class = forms.EquipmentSearchForm
    success_url = 'index'

    def get_queryset(self):
        return []

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            self.object_list = models.Equipment.objects.filter(vin__startswith=form.cleaned_data['vin'])
        else:
            self.object_list = []

        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))


class EquipmentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_Equipment'
    model = models.Equipment
    template_name = 'main/Equipment/new.html'
    form_class = forms.EquipmentCreateForm
    success_url = '/user_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vehicle_models'] = models.VehicleModel.objects.all()
        context['engine_models'] = models.EngineModel.objects.all()
        context['transmission_models'] = models.TransmissionModel.objects.all()
        context['drive_axles'] = models.DriveAxleModel.objects.all()
        context['steering_axles'] = models.SteeringAxleModel.objects.all()
        context['users'] = auth_models.CustomUser.objects.all()
        context['service_companies'] = models.ServiceCompany.objects.all()

        return context


class AdminIndexListView(PermissionRequiredMixin, ListView):
    model = models.Equipment
    permission_required = 'main.view_Equipment'
    template_name = 'main/user_index.html'
    context_object_name = 'Equipments'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        order_by = self.request.GET.get('order_by', 'shipment_date')

        if order_by in ['vehicle_model', 'engine_model', 'transmission_model', 'drive_axle_model',
                        'steerable_axle_model', 'service_company']:
            order_by = order_by + "__name"
        if order_by in ['customer']:
            order_by = "user__username"

        context['vm'] = self.request.GET.get('vm', '---')
        context['em'] = self.request.GET.get('em', '---')
        context['tr'] = self.request.GET.get('tr', '---')
        context['dam'] = self.request.GET.get('dam', '---')
        context['sam'] = self.request.GET.get('sam', '---')

        qs = qs_filter = models.Equipment.objects.all()
        if context['vm'] != "---":
            filter = models.VehicleModel.objects.get(name=context['vm']).pk
            qs = qs.filter(vehicle_model=filter)
        if context['em'] != "---":
            filter = models.EngineModel.objects.get(name=context['em']).pk
            qs = qs.filter(engine_model=filter)
        if context['tr'] != "---":
            filter = models.TransmissionModel.objects.get(name=context['tr']).pk
            qs = qs.filter(transmission_model=filter)
        if context['dam'] != "---":
            filter = models.DriveAxleModel.objects.get(name=context['dam']).pk
            qs = qs.filter(drive_axle=filter)
        if context['sam'] != "---":
            filter = models.SteeringAxleModel.objects.get(name=context['sam']).pk
            qs = qs.filter(steering_axle=filter)

        filter_list = ['vehicle_model', 'engine_model', 'transmission_model', 'drive_axle', 'steering_axle']

        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(name='manager').exists():
            context['Equipments'] = qs.order_by(order_by)
            for filter in filter_list:
                context[filter] = set(qs_filter.values_list(filter+'__name', flat=True))
        elif self.request.user.groups.filter(name='service_compamy').exists():
            context['Equipments'] = qs.filter(service_company__user=self.request.user.pk).order_by(order_by)
            for filter in filter_list:
                context[filter] = set(qs_filter.filter(service_company__user=self.request.user.pk).values_list(filter+'__name', flat=True))
        elif self.request.user.groups.filter(name='customer').exists():
            context['Equipments'] = qs.filter(user=self.request.user.id).order_by(order_by)
            for filter in filter_list:
                context[filter] = set(qs_filter.filter(user=self.request.user.id).values_list(filter+'__name', flat=True))
        else:
            context['Equipments'] = []

        return context


class EquipmentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'main.view_Equipment'
    model = models.Equipment
    queryset = models.Equipment.objects.all()
    template_name = 'main/Equipment/index.html'


class EquipmentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_Equipment'
    model = models.Equipment
    queryset = models.Equipment.objects.all()
    form_class = forms.EquipmentCreateForm
    template_name = 'main/Equipment/edit.html'
    success_url = '/user_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vehicle_models'] = models.VehicleModel.objects.all()
        context['engine_models'] = models.EngineModel.objects.all()
        context['transmission_models'] = models.TransmissionModel.objects.all()
        context['drive_axles'] = models.DriveAxleModel.objects.all()
        context['steering_axles'] = models.SteeringAxleModel.objects.all()
        context['users'] = auth_models.CustomUser.objects.all()
        context['service_companies'] = models.ServiceCompany.objects.all()

        return context


class EquipmentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'main.delete_Equipment'
    model = models.Equipment
    template_name = 'main/Equipment/delete.html'
    success_url = '/user_index'


def lookups(request):
    return render(request, 'main/lookups/list.html')


class VehicleModelListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_vehicle_model'
    model = models.VehicleModel
    queryset = models.VehicleModel.objects.all()
    template_name = 'main/lookups/vehicle_models/list.html'
    context_object_name = 'vehicle_models'


class VehicleModelCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_vehicle_model'
    model = models.VehicleModel
    form_class = forms.VehicleModelCreateForm
    template_name = 'main/lookups/vehicle_models/new.html'
    success_url = '/lookups/vehicle_models'


class VehicleModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_vehicle_model'
    model = models.VehicleModel
    queryset = models.VehicleModel.objects.all()
    form_class = forms.VehicleModelCreateForm
    template_name = 'main/lookups/vehicle_models/edit.html'
    success_url = '/lookups/vehicle_models'
    context_object_name = 'vehicle_model'


class EngineModelListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_Service'
    model = models.EngineModel
    queryset = models.EngineModel.objects.all()
    template_name = 'main/lookups/engine_models/list.html'
    context_object_name = 'engine_models'


class EngineModelCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_engine_model'
    model = models.EngineModel
    form_class = forms.EngineModelCreateForm
    template_name = 'main/lookups/engine_models/new.html'
    success_url = '/lookups/engine_models'


class EngineModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_engine_model'
    model = models.EngineModel
    queryset = models.EngineModel.objects.all()
    form_class = forms.EngineModelCreateForm
    template_name = 'main/lookups/engine_models/edit.html'
    success_url = '/lookups/engine_models'
    context_object_name = 'engine_model'


class TransmissionModelListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_transmission_model'
    model = models.TransmissionModel
    queryset = models.TransmissionModel.objects.all()
    template_name = 'main/lookups/transmission_models/list.html'
    context_object_name = 'transmission_models'


class TransmissionModelCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_transmission_model'
    model = models.TransmissionModel
    form_class = forms.TransmissionModelCreateForm
    template_name = 'main/lookups/transmission_models/new.html'
    success_url = '/lookups/transmission_models'


class TransmissionModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_transmission_model'
    model = models.TransmissionModel
    queryset = models.TransmissionModel.objects.all()
    form_class = forms.TransmissionModelCreateForm
    template_name = 'main/lookups/transmission_models/edit.html'
    success_url = '/lookups/transmission_models'
    context_object_name = 'transmission_model'


class DriveAxleListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_drive_axle_model'
    model = models.DriveAxleModel
    queryset = models.DriveAxleModel.objects.all()
    template_name = 'main/lookups/drive_axles/list.html'
    context_object_name = 'drive_axles'


class DriveAxleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_drive_axle_model'
    model = models.DriveAxleModel
    form_class = forms.DriveAxleModelCreateForm
    template_name = 'main/lookups/drive_axles/new.html'
    success_url = '/lookups/drive_axles'


class DriveAxleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_drive_axle_model'
    model = models.DriveAxleModel
    queryset = models.DriveAxleModel.objects.all()
    form_class = forms.DriveAxleModelCreateForm
    template_name = 'main/lookups/drive_axles/edit.html'
    success_url = '/lookups/drive_axles'
    context_object_name = 'drive_axle'


class SteeringAxleListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_steering_axle_model'
    model = models.SteeringAxleModel
    queryset = models.SteeringAxleModel.objects.all()
    template_name = 'main/lookups/steering_axles/list.html'
    context_object_name = 'steering_axles'


class SteeringAxleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_steering_axle_model'
    model = models.SteeringAxleModel
    form_class = forms.SteeringAxleModelCreateForm
    template_name = 'main/lookups/steering_axles/new.html'
    success_url = '/lookups/steering_axles'


class SteeringAxleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_steering_axle_model'
    model = models.SteeringAxleModel
    queryset = models.SteeringAxleModel.objects.all()
    form_class = forms.SteeringAxleModelCreateForm
    template_name = 'main/lookups/steering_axles/edit.html'
    success_url = '/lookups/steering_axles'
    context_object_name = 'steering_axle'


class ServiceCompanyListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_service_company'
    model = models.ServiceCompany
    queryset = models.ServiceCompany.objects.all()
    template_name = 'main/lookups/service_companies/list.html'
    context_object_name = 'service_companies'


class ServiceCompanyCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_service_company'
    model = models.ServiceCompany
    form_class = forms.ServiceCompanyCreateForm
    template_name = 'main/lookups/service_companies/new.html'
    success_url = '/lookups/service_companies'


class ServiceCompanyUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_service_company'
    model = models.ServiceCompany
    queryset = models.ServiceCompany.objects.all()
    form_class = forms.ServiceCompanyCreateForm
    template_name = 'main/lookups/service_companies/edit.html'
    success_url = '/lookups/service_companies'
    context_object_name = 'service_company'


class ServiceTypeListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_Service_type'
    model = models.ServiceType
    queryset = models.ServiceType.objects.all()
    template_name = 'main/lookups/Service_types/list.html'
    context_object_name = 'Service_types'


class ServiceTypeCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_Service_type'
    model = models.ServiceType
    form_class = forms.ServiceTypeCreateForm
    template_name = 'main/lookups/Service_types/new.html'
    success_url = '/lookups/Service_types'


class ServiceTypeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_Service_type'
    model = models.ServiceType
    queryset = models.ServiceType.objects.all()
    form_class = forms.ServiceTypeCreateForm
    template_name = 'main/lookups/Service_types/edit.html'
    success_url = '/lookups/Service_types'
    context_object_name = 'Service_type'


class DenialTypeListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_denial_type'
    model = models.DenialType
    queryset = models.DenialType.objects.all()
    template_name = 'main/lookups/denial_types/list.html'
    context_object_name = 'denial_types'


class DenialTypeCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_denial_type'
    model = models.DenialType
    form_class = forms.DenialTypeCreateForm
    template_name = 'main/lookups/denial_types/new.html'
    success_url = '/lookups/denial_types'


class DenialTypeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_denial_type'
    model = models.DenialType
    queryset = models.DenialType.objects.all()
    form_class = forms.DenialTypeCreateForm
    template_name = 'main/lookups/denial_types/edit.html'
    success_url = '/lookups/denial_types'
    context_object_name = 'denial_type'


class RecoveryMethodListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_recovery_method'
    model = models.RecoveryMethod
    queryset = models.RecoveryMethod.objects.all()
    template_name = 'main/lookups/recovery_methods/list.html'
    context_object_name = 'recovery_methods'


class RecoveryMethodCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_recovery_method'
    model = models.RecoveryMethod
    form_class = forms.RecoveryMethodCreateForm
    template_name = 'main/lookups/recovery_methods/new.html'
    success_url = '/lookups/recovery_methods'


class RecoveryMethodUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_recovery_method'
    model = models.RecoveryMethod
    queryset = models.RecoveryMethod.objects.all()
    form_class = forms.RecoveryMethodCreateForm
    template_name = 'main/lookups/recovery_methods/edit.html'
    success_url = '/lookups/recovery_methods'
    context_object_name = 'recovery_method'


class ServiceListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_Service'
    model = models.Service
    template_name = 'main/Service/list.html'
    context_object_name = 'Service_list'

    def get_queryset(self):
        queryset = models.Service.objects.select_related(
            'equipment', 'service_company', 'Service_type'
        ).all()

        # Получаем параметры фильтрации
        mt = self.request.GET.get('mt', '')  # Вид ТО
        cr = self.request.GET.get('cr', '')  # Машина (VIN)
        sc = self.request.GET.get('sc', '')  # Сервисная компания
        order_by = self.request.GET.get('order_by', '')  # Сортировка

        # Применяем фильтры
        if mt:
            queryset = queryset.filter(Service_type__name=mt)
        if cr:
            queryset = queryset.filter(equipment__vin=cr)  # Исправлено: equipment вместо Equipment
        if sc:
            queryset = queryset.filter(service_company__name=sc)

        # Применяем сортировку
        if order_by:
            # Обрабатываем сортировку по связанным полям
            if order_by == 'Equipment':
                order_by = 'equipment__vin'
            elif order_by == '-Equipment':
                order_by = '-equipment__vin'
            elif order_by == 'Service_type':
                order_by = 'Service_type__name'
            elif order_by == '-Service_type':
                order_by = '-Service_type__name'
            elif order_by == 'service_company':
                order_by = 'service_company__name'
            elif order_by == '-service_company':
                order_by = '-service_company__name'

            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('-Service_date')  # По умолчанию по дате

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Данные для селектов
        context['Equipment'] = models.Equipment.objects.values_list('vin', flat=True).distinct().order_by('vin')
        context['service_company'] = models.ServiceCompany.objects.values_list('name', flat=True).distinct().order_by(
            'name')
        context['Service_type'] = models.ServiceType.objects.values_list('name', flat=True).distinct().order_by('name')

        # Текущие значения фильтров для сохранения состояния
        context['current_mt'] = self.request.GET.get('mt', '')
        context['current_cr'] = self.request.GET.get('cr', '')
        context['current_sc'] = self.request.GET.get('sc', '')

        return context


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_Service'
    model = models.Service
    form_class = forms.ServiceCreateForm
    template_name = 'main/Service/new.html'
    success_url = '/Service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_Equipment'] = "Выберите машину"
        else:
            context['select_Equipment'] = models.Equipment.objects.get(id=id)

        context['Equipments'] = models.Equipment.objects.all()
        context['Service_types'] = models.ServiceType.objects.all()

        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')

        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = models.Equipment.objects.get(id=id).service_company.pk
            kwargs['initial'] = {'service_company': service_company, 'Equipment': id}
        return kwargs


class ServiceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'main.view_Service'
    model = models.Service
    template_name = 'main/Service/index.html'
    context_object_name = 'Service'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['Service_type'] = models.ServiceType.objects.all()
        context['service_company'] = models.ServiceCompany.objects.all()

        return context


class ClaimListView(PermissionRequiredMixin, ListView):
    permission_required = 'main.view_Claim'
    model = models.Claim
    queryset = models.Claim.objects.all()
    template_name = 'main/Claims/list.html'
    context_object_name = 'Claims'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Очистка фильтров - если нет GET параметров, очищаем сессию
        if not any([self.request.GET.get('fn'), self.request.GET.get('rm'), self.request.GET.get('sc'),
                    self.request.GET.get('order_by')]):
            self.request.session.pop('fn', None)
            self.request.session.pop('rm', None)
            self.request.session.pop('sc', None)

        # Явная очистка по кнопке "Сбросить"
        if self.request.GET.get('clear'):
            self.request.session.pop('order_by3', None)
            self.request.session.pop('fn', None)
            self.request.session.pop('rm', None)
            self.request.session.pop('sc', None)

        # Сортировка
        if self.request.GET.get('order_by'):
            self.request.session['order_by3'] = self.request.GET.get('order_by')

        if 'order_by3' not in self.request.session:
            self.request.session['order_by3'] = 'date_of_refusal'

        order_by = self.request.session['order_by3']
        if order_by in ['recovery_method', 'service_company', 'denial_type']:
            order_by = order_by + "__name"
        elif order_by == 'equipment':
            order_by = 'equipment__vin'

        # Фильтрация - сохраняем в сессию только если есть значение
        if self.request.GET.get('fn'):
            self.request.session['fn'] = self.request.GET.get('fn')
        elif self.request.GET.get('fn') == '':  # Если пустое значение - удаляем из сессии
            self.request.session.pop('fn', None)

        if self.request.GET.get('rm'):
            self.request.session['rm'] = self.request.GET.get('rm')
        elif self.request.GET.get('rm') == '':
            self.request.session.pop('rm', None)

        if self.request.GET.get('sc'):
            self.request.session['sc'] = self.request.GET.get('sc')
        elif self.request.GET.get('sc') == '':
            self.request.session.pop('sc', None)

        # Устанавливаем значения для контекста
        context['fn'] = self.request.session.get('fn', '---')
        context['rm'] = self.request.session.get('rm', '---')
        context['sc'] = self.request.session.get('sc', '---')  # ИСПРАВЛЕНО: было 'sc3'

        # Получаем базовый queryset
        qs = qs_filter = models.Claim.objects.all()

        # Применяем фильтры
        if 'fn' in self.request.session and self.request.session['fn'] != '---':
            qs = qs.filter(failure_node=self.request.session['fn'])

        if 'rm' in self.request.session and self.request.session['rm'] != '---':
            try:
                recovery_method = models.RecoveryMethod.objects.get(name=self.request.session['rm'])
                qs = qs.filter(recovery_method=recovery_method)
            except models.RecoveryMethod.DoesNotExist:
                self.request.session.pop('rm', None)
                context['rm'] = '---'

        if 'sc' in self.request.session and self.request.session['sc'] != '---':
            try:
                service_company = models.ServiceCompany.objects.get(name=self.request.session['sc'])
                qs = qs.filter(service_company=service_company)
            except models.ServiceCompany.DoesNotExist:
                self.request.session.pop('sc', None)
                context['sc'] = '---'

        # Применяем права доступа и формируем финальный результат
        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(
                name='manager').exists():
            context['failure_node'] = set(qs_filter.values_list('failure_node', flat=True))
            context['recovery_method'] = set(qs_filter.values_list('recovery_method__name', flat=True))
            context['service_company'] = set(qs_filter.values_list('service_company__name', flat=True))
            context['Claims'] = qs.order_by(order_by)
        elif self.request.user.groups.filter(name='service_company').exists():
            user_filter = qs_filter.filter(service_company__user=self.request.user)
            context['failure_node'] = set(user_filter.values_list('failure_node', flat=True))
            context['recovery_method'] = set(user_filter.values_list('recovery_method__name', flat=True))
            context['service_company'] = set(user_filter.values_list('service_company__name', flat=True))
            context['Claims'] = qs.filter(service_company__user=self.request.user).order_by(order_by)
        elif self.request.user.groups.filter(name='customer').exists():
            user_filter = qs_filter.filter(equipment__user=self.request.user)  # ИСПРАВЛЕНО: было Equipment__user
            context['failure_node'] = set(user_filter.values_list('failure_node', flat=True))
            context['recovery_method'] = set(user_filter.values_list('recovery_method__name', flat=True))
            context['service_company'] = set(user_filter.values_list('service_company__name', flat=True))
            context['Claims'] = qs.filter(equipment__user=self.request.user.id).order_by(
                order_by)  # ИСПРАВЛЕНО: было Equipment__user
        else:
            context['Claims'] = []
            context['failure_node'] = []
            context['recovery_method'] = []
            context['service_company'] = []

        return context


class ClaimCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.add_Claim'
    model = models.Claim
    form_class = forms.ClaimCreateForm
    template_name = 'main/Claims/new.html'
    success_url = '/Claims'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_Equipment'] = "Выберите машину"
        else:
            context['select_Equipment'] = models.Equipment.objects.get(id=id)

        context['denial_types'] = models.DenialType.objects.all()
        context['recovery_methods'] = models.RecoveryMethod.objects.all()
        context['service_companies'] = models.ServiceCompany.objects.all()
        context['Equipments'] = models.Equipment.objects.all()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')
        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = models.Equipment.objects.get(id=id).service_company.pk
            kwargs['initial'] = {'service_company': service_company, 'Equipment': id}
        return kwargs


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_Service'
    model = models.Service
    form_class = forms.ServiceCreateForm
    template_name = 'main/Service/edit.html'
    success_url = '/Service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_Equipment'] = "Выберите машину"
        else:
            context['select_Equipment'] = models.Equipment.objects.get(id=id)

        context['Equipments'] = models.Equipment.objects.all()

        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')

        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = models.Equipment.objects.get(id=id).service_company.pk
            kwargs['initial'] = {'service_company': service_company, 'Equipment': id}
        return kwargs


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'main.delete_Service'
    model = models.Service
    template_name = 'main/Service/delete.html'
    success_url = '/Service'


class ClaimUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_Claim'
    model = models.Claim
    form_class = forms.ClaimCreateForm
    template_name = 'main/Claims/edit.html'
    success_url = '/Claims'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.GET.get('id', '')
        if id == '':
            context['select_Equipment'] = "Выберите машину"
        else:
            context['select_Equipment'] = models.Equipment.objects.get(id=id)

        context['Equipments'] = models.Equipment.objects.all()
        context['denial_types'] = models.DenialType.objects.all()
        context['recovery_methods'] = models.RecoveryMethod.objects.all()

        return context


class ClaimDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'main.view_Claim'
    model = models.Claim
    template_name = 'main/Claims/index.html'
    context_object_name = 'Claim'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['service_company'] = models.ServiceCompany.objects.all()

        return context


class ClaimDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'main.delete_Claim'
    model = models.Claim
    template_name = 'main/Claims/delete.html'
    success_url = '/Claims'
