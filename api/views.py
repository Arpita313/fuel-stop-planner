from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_route, calculate_fuel_plan

class RouteOptimizerView(APIView):
    def get(self, request):
        start = request.query_params.get('start')
        finish = request.query_params.get('finish')

        if not start or not finish:
            return Response({"error": "Please provide start and finish coordinates in format: lon,lat"}, status=400)

        # Step 1: Get Route
        geometry, total_miles = get_route(start, finish)

        if geometry is None or total_miles == 0:
            return Response({"error": "Invalid coordinates or API limit reached."}, status=500)

        # Step 2: Calculate Plan
        try:
            fuel_stops, total_cost = calculate_fuel_plan(total_miles, geometry)
            
            return Response({
                "status": "success",
                "total_distance_miles": round(total_miles, 2),
                "total_fuel_cost": total_cost,
                "number_of_stops": len(fuel_stops),
                "fuel_stops": fuel_stops,
                "range_limit": "500 miles",
                "fuel_efficiency": "10 MPG"
            })
        except Exception as e:
            return Response({"error": f"Logic Error: {str(e)}"}, status=500)