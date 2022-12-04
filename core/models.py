from django.db import models


class TimeTracking(models.Model):
    """
        Abstract model to track date and time when records were created and updated.
    """
    created = models.DateTimeField("Date and time when the record was created", auto_now_add=True, blank=True,
                                   null=True)
    updated = models.DateTimeField(
        "Date and time the record was updated", auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class Weight(models.Model):
    """ Machine weight model """
    type = models.CharField("Type", max_length=20)
    unit = models.CharField("Unit", max_length=5)
    value = models.PositiveIntegerField("Value")

    class Meta:
        verbose_name = "Weight"
        verbose_name_plural = "Weights"

    def __str__(self) -> str:
        return f"Weight ID({self.id})"

    def create(data):
        return Weight.objects.create(
            type=data['type'],
            unit=data['unit'],
            value=data['value']
        )

class Car(models.Model):
    """ Machine model derived from the VIN data """
    vin = models.CharField("VIN code", max_length=17)
    year = models.CharField("Year", max_length=4)
    make = models.CharField("Make", max_length=20)
    model = models.CharField("Model", max_length=20)
    type = models.CharField("Type", max_length=20)
    color = models.CharField("Color", max_length=20)
    weight = models.ForeignKey(
        to="Weight", on_delete=models.SET_NULL, null=True)
    dimension = models.JSONField("Dimension")

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self) -> str:
        return f"Car ID({self.id})"

    def create(data, weight):
        return Car.objects.create(
            vin=data.get('VIN'),
            year=data.get('vehicle')[0].get('year'),
            make=data.get('vehicle')[0].get('make'),
            model=data.get('vehicle')[0].get('model'),
            type=data.get('vehicle')[0].get('trim'),
            color=data.get('vehicle')[0].get('color'),
            weight=weight,
            dimension=data.get('vehicle')[0].get('dimensions'),
        )

    
