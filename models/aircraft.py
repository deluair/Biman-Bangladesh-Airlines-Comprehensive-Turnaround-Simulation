from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Aircraft:
    """Represents an individual aircraft in the fleet."""
    registration: str
    type: str
    age: float  # in years
    purchase_date: datetime
    last_maintenance: datetime
    next_maintenance: datetime
    status: str  # 'active', 'maintenance', 'grounded'
    utilization_hours: float  # daily block hours
    fuel_efficiency: float  # liters per block hour
    seating_capacity: int
    cargo_capacity: float  # in kg
    
    def calculate_maintenance_cost(self) -> float:
        """Calculate estimated maintenance cost based on age and utilization."""
        base_cost = 100000  # Base cost in USD
        age_factor = 1 + (self.age * 0.1)  # 10% increase per year
        utilization_factor = 1 + (self.utilization_hours * 0.05)  # 5% increase per block hour
        return base_cost * age_factor * utilization_factor
    
    def calculate_fuel_consumption(self, block_hours: float) -> float:
        """Calculate fuel consumption for given block hours."""
        return block_hours * self.fuel_efficiency
    
    def needs_maintenance(self) -> bool:
        """Check if aircraft needs maintenance based on utilization and time."""
        return (datetime.now() - self.last_maintenance).days >= 30 or \
               self.utilization_hours >= 100  # Maintenance every 100 block hours
    
    def update_status(self, new_status: str):
        """Update aircraft status."""
        valid_statuses = ['active', 'maintenance', 'grounded']
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        self.status = new_status 