from django.urls import path
from .views import RouteOptimizerView  # Isse check karo, pehle yahan FuelOptimizerView hoga

urlpatterns = [
    path('route-optimizer/', RouteOptimizerView.as_view(), name='route-optimizer'),
]