from django.urls import path
from .views import FuelOptimizerView

urlpatterns = [
    path('route-optimizer/', FuelOptimizerView.as_view()),
]