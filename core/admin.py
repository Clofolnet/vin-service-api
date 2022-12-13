from django.contrib import admin

from .models import Car, Weight


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    pass
