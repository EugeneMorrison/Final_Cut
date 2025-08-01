# Generated by Django 5.0.6 on 2025-07-26 19:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DenialType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Характер отказа',
                'verbose_name_plural': 'Характеры отказов',
            },
        ),
        migrations.CreateModel(
            name='DriveAxleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель ведущего моста',
                'verbose_name_plural': 'Модели ведущего моста',
            },
        ),
        migrations.CreateModel(
            name='EngineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель двигателя',
                'verbose_name_plural': 'Модели двигателя',
            },
        ),
        migrations.CreateModel(
            name='FailureNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Узел отказа',
                'verbose_name_plural': 'Узлы отказа',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Вид ТО',
                'verbose_name_plural': 'Виды ТО',
            },
        ),
        migrations.CreateModel(
            name='RecoveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Способ восстановления',
                'verbose_name_plural': 'Способы восстановления',
            },
        ),
        migrations.CreateModel(
            name='SteeringAxleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель управляемого моста',
                'verbose_name_plural': 'Модели управляемого моста',
            },
        ),
        migrations.CreateModel(
            name='TransmissionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель трансмиссии',
                'verbose_name_plural': 'Модели трансмиссии',
            },
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель техники',
                'verbose_name_plural': 'Модели техники',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=255, verbose_name='Зав. № машины')),
                ('engine_number', models.CharField(max_length=255, verbose_name='Зав. № двигателя')),
                ('transmission_number', models.CharField(max_length=255, verbose_name='Зав. № трансмиссии')),
                ('drive_axle_number', models.CharField(max_length=255, verbose_name='Зав. № ведущего моста')),
                ('steering_axle_number', models.CharField(max_length=255, verbose_name='Зав. № управляемого моста')),
                ('supply_agreement', models.TextField(verbose_name='Договор поставки')),
                ('shipment_date', models.DateField(verbose_name='Дата отгрузки с завода')),
                ('consignee', models.TextField(verbose_name='Грузополучатель')),
                ('delivery_address', models.TextField(verbose_name='Адрес поставки (эксплуатации)')),
                ('equipment', models.TextField(verbose_name='Комплектация, доп. опции')),
                ('warranty_end_date', models.DateField(blank=True, null=True, verbose_name='Дата окончания гарантии')),
                ('client_comment', models.TextField(blank=True, null=True, verbose_name='Комментарий клиента')),
                ('drive_axle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='main.driveaxlemodel')),
                ('engine_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='main.enginemodel')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_equipments', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный менеджер')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудование',
            },
        ),
        migrations.CreateModel(
            name='ServiceCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сервисная компания',
                'verbose_name_plural': 'Сервисные компании',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Service_date', models.DateField(verbose_name='Дата проведения ТО')),
                ('operating_time', models.IntegerField(verbose_name='Наработка мото/часов')),
                ('order', models.CharField(max_length=50, verbose_name='Номер заказа наряда')),
                ('order_date', models.DateField(verbose_name='Дата заказа-наряда')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Service_logs', to='main.equipment')),
                ('Service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Service_logs', to='main.Servicetype')),
                ('service_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Service_logs', to='main.servicecompany')),
            ],
            options={
                'verbose_name': 'Техническое обслуживание (ТО)',
                'verbose_name_plural': 'Техническое обслуживание (ТО)',
                'ordering': ('Service_date',),
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='main.servicecompany', verbose_name='Сервисная компания'),
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_refusal', models.DateField(verbose_name='Дата отказа')),
                ('operating_time', models.IntegerField(verbose_name='Наработка м/час')),
                ('failure_node', models.TextField(verbose_name='Узел отказа')),
                ('used_details', models.TextField(blank=True, verbose_name='Используемые запасные части')),
                ('date_of_restoration', models.DateField(verbose_name='Дата восстановления')),
                ('equipment_downtime', models.TextField(verbose_name='Время простоя техники')),
                ('denial_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Claim_logs', to='main.denialtype', verbose_name='Характер отказа')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Claim_logs', to='main.equipment')),
                ('recovery_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Claim_logs', to='main.recoverymethod', verbose_name='Способ восстановления')),
                ('service_company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Claim_logs', to='main.servicecompany', verbose_name='Сервисная компания')),
            ],
            options={
                'verbose_name': 'Рекламация',
                'verbose_name_plural': 'Рекламации',
                'ordering': ['date_of_refusal'],
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='steering_axle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='main.steeringaxlemodel'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='transmission_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='main.transmissionmodel'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='vehicle_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='main.vehiclemodel'),
        ),
    ]
