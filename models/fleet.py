from typing import List, Dict
from datetime import datetime
from .aircraft import Aircraft

class Fleet:
    """Manages the entire aircraft fleet of Biman Bangladesh Airlines."""
    
    def __init__(self):
        self.aircraft: List[Aircraft] = []
        self.fleet_composition: Dict[str, int] = {
            'B777-300ER': 4,
            'B787-8': 4,
            'B787-9': 2,
            'B737-800': 6,
            'Dash8-Q400': 5
        }
        self.initialize_fleet()
    
    def initialize_fleet(self):
        """Initialize the fleet with realistic aircraft data."""
        # B777-300ER fleet
        for i in range(4):
            self.aircraft.append(Aircraft(
                registration=f'S2-{i+1}',
                type='B777-300ER',
                age=10.0,
                purchase_date=datetime(2015, 1, 1),
                last_maintenance=datetime.now(),
                next_maintenance=datetime.now(),
                status='active',
                utilization_hours=10.5,
                fuel_efficiency=8500,  # liters per block hour
                seating_capacity=419,
                cargo_capacity=50000
            ))
        
        # B787-8 fleet
        for i in range(4):
            self.aircraft.append(Aircraft(
                registration=f'S2-{i+5}',
                type='B787-8',
                age=7.0,
                purchase_date=datetime(2018, 1, 1),
                last_maintenance=datetime.now(),
                next_maintenance=datetime.now(),
                status='active',
                utilization_hours=11.0,
                fuel_efficiency=4500,
                seating_capacity=271,
                cargo_capacity=35000
            ))
        
        # B787-9 fleet
        for i in range(2):
            self.aircraft.append(Aircraft(
                registration=f'S2-{i+9}',
                type='B787-9',
                age=5.5,
                purchase_date=datetime(2020, 1, 1),
                last_maintenance=datetime.now(),
                next_maintenance=datetime.now(),
                status='active',
                utilization_hours=11.5,
                fuel_efficiency=4800,
                seating_capacity=298,
                cargo_capacity=40000
            ))
        
        # B737-800 fleet
        for i in range(6):
            self.aircraft.append(Aircraft(
                registration=f'S2-{i+11}',
                type='B737-800',
                age=13.5,
                purchase_date=datetime(2012, 1, 1),
                last_maintenance=datetime.now(),
                next_maintenance=datetime.now(),
                status='active',
                utilization_hours=9.5,
                fuel_efficiency=2500,
                seating_capacity=189,
                cargo_capacity=20000
            ))
        
        # Dash8-Q400 fleet
        for i in range(5):
            self.aircraft.append(Aircraft(
                registration=f'S2-{i+17}',
                type='Dash8-Q400',
                age=8.0,
                purchase_date=datetime(2017, 1, 1),
                last_maintenance=datetime.now(),
                next_maintenance=datetime.now(),
                status='active',
                utilization_hours=8.5,
                fuel_efficiency=1200,
                seating_capacity=78,
                cargo_capacity=8000
            ))
    
    def get_available_aircraft(self, aircraft_type: str = None) -> List[Aircraft]:
        """Get list of available aircraft, optionally filtered by type."""
        available = [a for a in self.aircraft if a.status == 'active']
        if aircraft_type:
            available = [a for a in available if a.type == aircraft_type]
        return available
    
    def get_maintenance_aircraft(self) -> List[Aircraft]:
        """Get list of aircraft currently in maintenance."""
        return [a for a in self.aircraft if a.status == 'maintenance']
    
    def get_grounded_aircraft(self) -> List[Aircraft]:
        """Get list of grounded aircraft."""
        return [a for a in self.aircraft if a.status == 'grounded']
    
    def calculate_total_maintenance_cost(self) -> float:
        """Calculate total maintenance cost for the fleet."""
        return sum(aircraft.calculate_maintenance_cost() for aircraft in self.aircraft)
    
    def calculate_total_fuel_consumption(self) -> float:
        """Calculate total fuel consumption for the fleet."""
        return sum(aircraft.calculate_fuel_consumption(aircraft.utilization_hours) 
                  for aircraft in self.aircraft)
    
    def get_fleet_utilization(self) -> float:
        """Calculate average fleet utilization in block hours per day."""
        active_aircraft = [a for a in self.aircraft if a.status == 'active']
        if not active_aircraft:
            return 0.0
        return sum(a.utilization_hours for a in active_aircraft) / len(active_aircraft) 