from rest_framework import serializers

from .models import Car, Weight


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    weight = WeightSerializer(read_only=True)

    class Meta:
        model = Car
        fields = "__all__"
