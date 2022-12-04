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

	""" def create(self, validated_data):
        weight = Weight.objects.get(pk=validated_data.get('weight'))
        instance = Equipment.objects.create(**validated_data)
        Assignment.objects.create(Order=order, Equipment=instance)
        return instance """
