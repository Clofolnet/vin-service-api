from django.urls import path

from .views import (CarDetailView, CarListView, DecodeVINView,
                    WeightDetailView, WeightListView, vin_decode)

urlpatterns = [
    path('vin-decode-views-style/<str:vin_code>/', vin_decode),
    path('vin-decode-class-based-style/<str:vin_code>/',
         DecodeVINView.as_view(), name="vin-decode-class-based-style"),
    path('cars/', CarListView.as_view(), name="cars"),
    path('cars/<int:pk>/', CarDetailView.as_view(), name="cars-detail"),
    path('weights/', WeightListView.as_view(), name="weights"),
    path('weights/<int:pk>/', WeightDetailView.as_view(), name="weights-detail"),
]
