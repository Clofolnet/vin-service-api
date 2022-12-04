from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, Weight
from .serializers import CarSerializer, WeightSerializer
from .services import get_decode_vim_code


@api_view(['GET'])
def vim_decode(request, vim_code):
	decode_data = get_decode_vim_code(vim_code)
	if not decode_data:
		return Response({'success': False, 'message': "Wrong request to VIM decoder"})
	try:
		with transaction.atomic():
			weight = Weight.create(decode_data.get('decode').get('vehicle')[0].get('weight'))
			car = Car.create(decode_data.get('decode'), weight)

		data = CarSerializer(car).data
		return Response({'success': True, 'message': "Decoding successfully", 'decode_data':data})
	except:
		return Response({'success': False, 'message': "Failed to save data in the database"})

class CarListView(APIView):
    """
    	List all cars, create a new car
    """
    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.error_messages, serializer._errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDetailView(APIView):
    """ CRUD for Car objects """

    def get_object(self, pk):
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def put(self, request, pk):
        car = self.get_object(pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WeightListView(APIView):
    """
    	List all weight, create a new weight entry
    """
    def get(self, request, format=None):
        weights = Weight.objects.all()
        serializer = WeightSerializer(weights, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WeightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeightDetailView(APIView):
    """ CRUD for Weight object """

    def get_object(self, pk):
        try:
            return Weight.objects.get(pk=pk)
        except Weight.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            weight = self.get_object(pk)
            serializer = WeightSerializer(weight)
            return Response(serializer.data)
        except Weight.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        weight = self.get_object(pk)
        serializer = WeightSerializer(weight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        weight = self.get_object(pk)
        weight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)