from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_route, calculate_fuel_plan

class FuelOptimizerView(APIView):
    def get(self, request):
        start = request.query_params.get('start')
        finish = request.query_params.get('finish')
        
        geometry, miles = get_route(start, finish)
        
        # Agar rasta nahi mila toh error dikhao
        if geometry is None or miles == 0:
            return Response({"error": "Could not calculate route. Check API Key or Coords."}, status=400)
            
        stops, cost = calculate_fuel_plan(miles)
        
        return Response({
            "total_distance_miles": round(miles, 2),
            "estimated_total_cost": cost,
            "recommended_stops": stops
        })