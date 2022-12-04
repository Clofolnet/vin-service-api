from django.urls import path

from .views import (CarDetailView, CarListView, WeightDetailView,
                    WeightListView, vim_decode)

urlpatterns = [
    path('vim_decode/<str:vim_code>/', vim_decode),
    path('cars/', CarListView.as_view(), name="cars"),
    path('cars/<int:pk>/', CarDetailView.as_view(), name="cars-detail"),
    path('weights/', WeightListView.as_view(), name="weights"),
    path('weights/<int:pk>/', WeightDetailView.as_view(), name="weights-detail"),
]


