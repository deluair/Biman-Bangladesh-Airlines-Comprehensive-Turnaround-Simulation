from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Route:
    """Represents an airline route with its performance metrics."""
    origin: str
    destination: str
    distance: float  # in kilometers
    flight_time: float  # in hours
    frequency: int  # flights per week
    aircraft_type: str
    load_factor: float  # percentage
    yield_per_rpk: float  # revenue per revenue passenger kilometer
    operating_cost_per_ask: float  # cost per available seat kilometer
    fuel_price: float  # per liter
    ground_handling_cost: float  # per flight
    airport_charges: float  # per flight
    crew_cost: float  # per flight
    maintenance_cost: float  # per flight
    marketing_cost: float  # per flight
    other_costs: float  # per flight
    
    def calculate_revenue(self, seats: int) -> float:
        """Calculate revenue for a single flight."""
        passengers = seats * self.load_factor
        rpk = passengers * self.distance
        return rpk * self.yield_per_rpk
    
    def calculate_operating_cost(self, seats: int) -> float:
        """Calculate operating cost for a single flight."""
        ask = seats * self.distance
        base_cost = ask * self.operating_cost_per_ask
        return base_cost + self.ground_handling_cost + self.airport_charges + \
               self.crew_cost + self.maintenance_cost + self.marketing_cost + self.other_costs
    
    def calculate_profit(self, seats: int) -> float:
        """Calculate profit for a single flight."""
        revenue = self.calculate_revenue(seats)
        cost = self.calculate_operating_cost(seats)
        return revenue - cost
    
    def calculate_weekly_profit(self, seats: int) -> float:
        """Calculate weekly profit for the route."""
        return self.calculate_profit(seats) * self.frequency
    
    def calculate_break_even_load_factor(self, seats: int) -> float:
        """Calculate break-even load factor for the route."""
        total_cost = self.calculate_operating_cost(seats)
        revenue_per_passenger = self.yield_per_rpk * self.distance
        break_even_passengers = total_cost / revenue_per_passenger
        return break_even_passengers / seats

class RouteNetwork:
    """Manages the entire route network of Biman Bangladesh Airlines."""
    
    def __init__(self):
        self.routes: Dict[str, Route] = {}
        self.initialize_routes()
    
    def initialize_routes(self):
        """Initialize the route network with realistic data."""
        # Domestic routes
        self.add_route(Route(
            origin='DAC',  # Dhaka
            destination='CGP',  # Chittagong
            distance=250,
            flight_time=0.75,
            frequency=14,
            aircraft_type='Dash8-Q400',
            load_factor=0.75,
            yield_per_rpk=0.12,
            operating_cost_per_ask=0.08,
            fuel_price=1.2,
            ground_handling_cost=1000,
            airport_charges=500,
            crew_cost=800,
            maintenance_cost=500,
            marketing_cost=200,
            other_costs=300
        ))
        
        self.add_route(Route(
            origin='DAC',
            destination='ZYL',  # Sylhet
            distance=200,
            flight_time=0.5,
            frequency=7,
            aircraft_type='Dash8-Q400',
            load_factor=0.70,
            yield_per_rpk=0.11,
            operating_cost_per_ask=0.08,
            fuel_price=1.2,
            ground_handling_cost=1000,
            airport_charges=500,
            crew_cost=800,
            maintenance_cost=500,
            marketing_cost=200,
            other_costs=300
        ))
        
        # Middle East routes
        self.add_route(Route(
            origin='DAC',
            destination='DXB',  # Dubai
            distance=3500,
            flight_time=5.5,
            frequency=7,
            aircraft_type='B777-300ER',
            load_factor=0.85,
            yield_per_rpk=0.15,
            operating_cost_per_ask=0.10,
            fuel_price=1.2,
            ground_handling_cost=5000,
            airport_charges=3000,
            crew_cost=4000,
            maintenance_cost=2000,
            marketing_cost=1000,
            other_costs=1500
        ))
        
        self.add_route(Route(
            origin='DAC',
            destination='AUH',  # Abu Dhabi
            distance=3400,
            flight_time=5.0,
            frequency=5,
            aircraft_type='B787-8',
            load_factor=0.82,
            yield_per_rpk=0.14,
            operating_cost_per_ask=0.09,
            fuel_price=1.2,
            ground_handling_cost=4500,
            airport_charges=2800,
            crew_cost=3500,
            maintenance_cost=1800,
            marketing_cost=900,
            other_costs=1200
        ))
        
        # Asian routes
        self.add_route(Route(
            origin='DAC',
            destination='SIN',  # Singapore
            distance=2800,
            flight_time=4.5,
            frequency=7,
            aircraft_type='B787-8',
            load_factor=0.80,
            yield_per_rpk=0.14,
            operating_cost_per_ask=0.09,
            fuel_price=1.2,
            ground_handling_cost=4000,
            airport_charges=2500,
            crew_cost=3500,
            maintenance_cost=1800,
            marketing_cost=800,
            other_costs=1200
        ))
        
        self.add_route(Route(
            origin='DAC',
            destination='KUL',  # Kuala Lumpur
            distance=2600,
            flight_time=4.0,
            frequency=5,
            aircraft_type='B787-8',
            load_factor=0.78,
            yield_per_rpk=0.13,
            operating_cost_per_ask=0.09,
            fuel_price=1.2,
            ground_handling_cost=3800,
            airport_charges=2300,
            crew_cost=3300,
            maintenance_cost=1700,
            marketing_cost=700,
            other_costs=1100
        ))
        
        # European routes
        self.add_route(Route(
            origin='DAC',
            destination='LHR',  # London
            distance=8000,
            flight_time=10.0,
            frequency=3,
            aircraft_type='B777-300ER',
            load_factor=0.75,
            yield_per_rpk=0.18,
            operating_cost_per_ask=0.12,
            fuel_price=1.2,
            ground_handling_cost=8000,
            airport_charges=5000,
            crew_cost=6000,
            maintenance_cost=3000,
            marketing_cost=2000,
            other_costs=2500
        ))
        
        self.add_route(Route(
            origin='DAC',
            destination='MAN',  # Manchester
            distance=7800,
            flight_time=9.5,
            frequency=2,
            aircraft_type='B777-300ER',
            load_factor=0.70,
            yield_per_rpk=0.17,
            operating_cost_per_ask=0.12,
            fuel_price=1.2,
            ground_handling_cost=7500,
            airport_charges=4800,
            crew_cost=5800,
            maintenance_cost=2900,
            marketing_cost=1800,
            other_costs=2300
        ))
        
        # Loss-making routes (to be addressed in turnaround)
        self.add_route(Route(
            origin='DAC',
            destination='NRT',  # Tokyo Narita
            distance=5000,
            flight_time=7.0,
            frequency=0,  # Suspended
            aircraft_type='B787-9',
            load_factor=0.65,
            yield_per_rpk=0.16,
            operating_cost_per_ask=0.11,
            fuel_price=1.2,
            ground_handling_cost=6000,
            airport_charges=4000,
            crew_cost=4500,
            maintenance_cost=2200,
            marketing_cost=1500,
            other_costs=1800
        ))
        
        # Regional routes
        self.add_route(Route(
            origin='DAC',
            destination='DEL',  # Delhi
            distance=1500,
            flight_time=2.5,
            frequency=4,
            aircraft_type='B737-800',
            load_factor=0.72,
            yield_per_rpk=0.13,
            operating_cost_per_ask=0.09,
            fuel_price=1.2,
            ground_handling_cost=2500,
            airport_charges=1500,
            crew_cost=2000,
            maintenance_cost=1000,
            marketing_cost=500,
            other_costs=800
        ))
        
        self.add_route(Route(
            origin='DAC',
            destination='CCU',  # Kolkata
            distance=500,
            flight_time=1.0,
            frequency=7,
            aircraft_type='B737-800',
            load_factor=0.75,
            yield_per_rpk=0.12,
            operating_cost_per_ask=0.08,
            fuel_price=1.2,
            ground_handling_cost=2000,
            airport_charges=1200,
            crew_cost=1500,
            maintenance_cost=800,
            marketing_cost=400,
            other_costs=600
        ))
    
    def add_route(self, route: Route):
        """Add a new route to the network."""
        route_key = f"{route.origin}-{route.destination}"
        self.routes[route_key] = route
    
    def get_route(self, origin: str, destination: str) -> Optional[Route]:
        """Get route information for a specific origin-destination pair."""
        route_key = f"{origin}-{destination}"
        return self.routes.get(route_key)
    
    def get_profitable_routes(self) -> List[Route]:
        """Get list of profitable routes."""
        return [route for route in self.routes.values() 
                if route.calculate_weekly_profit(route.aircraft_type) > 0]
    
    def get_unprofitable_routes(self) -> List[Route]:
        """Get list of unprofitable routes."""
        return [route for route in self.routes.values() 
                if route.calculate_weekly_profit(route.aircraft_type) <= 0]
    
    def calculate_total_network_profit(self) -> float:
        """Calculate total profit for the entire network."""
        return sum(route.calculate_weekly_profit(route.aircraft_type) 
                  for route in self.routes.values()) 