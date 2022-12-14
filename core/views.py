from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, Weight
from .serializers import CarSerializer, WeightSerializer
from .services import get_decode_vin_code, save_decoding_data


@api_view(['GET'])
def vin_decode(request, vin_code):
    try:
        response_data = {}
        request_status = None
        if Car.uniqueness_check_by_vin_code(vin_code):
            car = Car.get_car_by_vin_code(vin_code)
            request_status = status.HTTP_200_OK
            response_data.update(
                {'success': True, 'message': "The record has already been created, the data from the database has been returned"})
        else:
            decode_data = get_decode_vin_code(vin_code)
            if decode_data:
                car = save_decoding_data(decode_data)
                request_status = status.HTTP_201_CREATED
                response_data.update(
                    {'success': True, 'message': "Decoding successfully"})
            else:
                car = None
                request_status = status.HTTP_400_BAD_REQUEST
                response_data.update(
                    {'success': False, 'message': "Wrong request to VIM decoder"})

        if car != None:
            data = CarSerializer(car).data
            response_data.update({'data': data})

    except Exception as e:
        response_data = {'success': False, 'message': str(Exception)}

    finally:
        if request_status is None:
            request_status = status.HTTP_400_BAD_REQUEST
        return Response(response_data, status=request_status)


class DecodeVINView(APIView):
    """  
            Decode VIN code
    """

    def get(self, request, vin_code):
        try:
            response_data = {}
            request_status = None
            if Car.uniqueness_check_by_vin_code(vin_code):
                car = Car.get_car_by_vin_code(vin_code)
                request_status = status.HTTP_200_OK
                response_data.update(
                    {'success': True, 'message': "The record has already been created, the data from the database has been returned"})
            else:
                decode_data = get_decode_vin_code(vin_code)
                if decode_data:
                    car = save_decoding_data(decode_data)
                    request_status = status.HTTP_201_CREATED
                    response_data.update(
                        {'success': True, 'message': "Decoding successfully"})
                else:
                    car = None
                    request_status = status.HTTP_400_BAD_REQUEST
                    response_data.update(
                        {'success': False, 'message': "Wrong request to VIM decoder"})

            if car != None:
                data = CarSerializer(car).data
                response_data.update({'data': data})

        except Exception as e:
            response_data = {'success': False, 'message': str(e)}

        finally:
            if request_status is None:
                request_status = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status=request_status)


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
