from django.db import models
from authentication import models as auth_models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class VehicleModel(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"


class EngineModel(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модель двигателя"
        verbose_name_plural = "Модели двигателя"


class TransmissionModel(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модель трансмиссии"
        verbose_name_plural = "Модели трансмиссии"


class DriveAxleModel(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модель ведущего моста"
        verbose_name_plural = "Модели ведущего моста"


class SteeringAxleModel(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модель управляемого моста"
        verbose_name_plural = "Модели управляемого моста"


class ServiceCompany(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    user = models.OneToOneField(auth_models.CustomUser, on_delete=models.SET_NULL,
                                 verbose_name='Пользователь', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сервисная компания"
        verbose_name_plural = "Сервисные компании"


class FailureNode(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Узел отказа"
        verbose_name_plural = "Узлы отказа"


class RecoveryMethod(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Способ восстановления"
        verbose_name_plural = "Способы восстановления"


class ServiceType(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид ТО"
        verbose_name_plural = "Виды ТО"


# --- Машина → Оборудование ---
class Equipment(models.Model):
    vin = models.CharField("Зав. № машины", max_length=255)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name="equipments")
    engine_model = models.ForeignKey(EngineModel, on_delete=models.CASCADE, related_name="equipments")
    engine_number = models.CharField("Зав. № двигателя", max_length=255)
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.CASCADE, related_name="equipments")
    transmission_number = models.CharField("Зав. № трансмиссии", max_length=255)
    drive_axle = models.ForeignKey(DriveAxleModel, on_delete=models.CASCADE, related_name="equipments")
    drive_axle_number = models.CharField("Зав. № ведущего моста", max_length=255)
    steering_axle = models.ForeignKey(SteeringAxleModel, on_delete=models.CASCADE, related_name="equipments")
    steering_axle_number = models.CharField("Зав. № управляемого моста", max_length=255)

    supply_agreement = models.TextField("Договор поставки")
    shipment_date = models.DateField("Дата отгрузки с завода")
    consignee = models.TextField("Грузополучатель")
    delivery_address = models.TextField("Адрес поставки (эксплуатации)")
    equipment = models.TextField("Комплектация, доп. опции")

    user = models.ForeignKey(auth_models.CustomUser, on_delete=models.CASCADE,
                             verbose_name="Клиент", related_name="equipments")
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE,
                                        verbose_name="Сервисная компания", related_name="equipments")

    # Новые поля
    warranty_end_date = models.DateField("Дата окончания гарантии", null=True, blank=True)
    manager = models.ForeignKey(auth_models.CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="managed_equipments", verbose_name="Ответственный менеджер")
    client_comment = models.TextField("Комментарий клиента", blank=True, null=True)

    def __str__(self):
        return self.vin

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"

class EquipmentListView(LoginRequiredMixin, ListView):
    template_name = 'user_index.html'
    model = Equipment
    context_object_name = 'equipments'

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.groups.filter(name='manager').exists():
            return qs

        if user.groups.filter(name='customer').exists():
            return qs.filter(client=user.customer)

        if user.groups.filter(name='service_company').exists():
            # фильтруем по полю service_company в модели Equipment
            return qs.filter(service_company=user.servicecompany)

        return qs.none()
# --- ТО ---
class Service(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="Service_logs")
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, related_name="Service_logs")
    Service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name="Service_logs")

    Service_date = models.DateField(verbose_name='Дата проведения ТО')
    operating_time = models.IntegerField(verbose_name='Наработка мото/часов')
    order = models.CharField(max_length=50, verbose_name='Номер заказа наряда')
    order_date = models.DateField(verbose_name='Дата заказа-наряда')

    def __str__(self):
        return f"{self.equipment.vin} / {self.Service_type.name}"

    class Meta:
        verbose_name = 'Техническое обслуживание (ТО)'
        verbose_name_plural = 'Техническое обслуживание (ТО)'
        ordering = ('Service_date',)


# --- Характер отказа ---
class DenialType(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характер отказа'
        verbose_name_plural = 'Характеры отказов'


# --- Рекламации ---
class Claim(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="Claim_logs")
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.SET_NULL,
                                        verbose_name='Сервисная компания', null=True, related_name="Claim_logs")

    date_of_refusal = models.DateField(verbose_name='Дата отказа')
    operating_time = models.IntegerField(verbose_name='Наработка м/час')
    failure_node = models.TextField(verbose_name='Узел отказа')
    denial_type = models.ForeignKey(DenialType, on_delete=models.CASCADE, verbose_name='Характер отказа',
                                    related_name="Claim_logs")
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.CASCADE,
                                        verbose_name='Способ восстановления', related_name="Claim_logs")

    used_details = models.TextField(blank=True, verbose_name='Используемые запасные части')
    date_of_restoration = models.DateField(verbose_name='Дата восстановления')
    equipment_downtime = models.TextField(verbose_name='Время простоя техники')

    def __str__(self):
        return f"{self.equipment.vin} / {self.failure_node}"

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'
        ordering = ['date_of_refusal']
