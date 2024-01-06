# Generated by Django 4.2.6 on 2023-10-28 13:40

from django.db import migrations


def set_price(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')

    for smartphone in smartphone_model.objects.all():
        smartphone.price = len(smartphone.brand) * 120
        smartphone.save()


def set_category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')

    for smartphone in smartphone_model.objects.all():
        if smartphone.price >= 750:
            smartphone.category = "Expensive"
        else:
            smartphone.category = "Cheap"
        smartphone.save()


def set_category_and_price(apps, schema_editor):
    set_price(apps, schema_editor)
    set_category(apps, schema_editor)


def reverse_code(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')

    for smartphone in smartphone_model.objects.all():
        smartphone.price = 1
        smartphone.category = "empty"
        smartphone.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_smartphone'),
    ]

    operations = [
        migrations.RunPython(set_category_and_price, reverse_code=reverse_code),
    ]