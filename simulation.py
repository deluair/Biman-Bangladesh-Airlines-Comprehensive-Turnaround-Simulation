from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import logging
from models.aircraft import Aircraft
from models.fleet import Fleet
from models.route import Route, RouteNetwork
from models.financial import FinancialModel, FinancialMetrics

class BimanSimulation:
    """Main simulation engine for Biman Bangladesh Airlines turnaround."""
    
    def __init__(self):
        self.fleet = Fleet()
        self.route_network = RouteNetwork()
        self.financial_model = FinancialModel()
        self.current_quarter = "2025-Q1"
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('simulation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BimanSimulation')
    
    def run_quarter(self, quarter: str, actions: Dict) -> Dict:
        """Run simulation for a single quarter with given actions."""
        self.logger.info(f"Running simulation for {quarter}")
        
        # Apply actions
        self._apply_actions(actions)
        
        # Calculate route performance
        route_performance = self._calculate_route_performance()
        
        # Update financial metrics
        financial_metrics = self._update_financials(quarter, route_performance)
        
        # Generate quarterly report
        report = self._generate_quarterly_report(quarter, route_performance, financial_metrics)
        
        self.current_quarter = quarter
        return report
    
    def _apply_actions(self, actions: Dict):
        """Apply simulation actions for the quarter."""
        # Route changes
        if 'route_changes' in actions:
            for change in actions['route_changes']:
                if change['action'] == 'add':
                    self.route_network.add_route(Route(**change['route_data']))
                elif change['action'] == 'modify':
                    route = self.route_network.get_route(change['origin'], change['destination'])
                    if route:
                        for key, value in change['modifications'].items():
                            setattr(route, key, value)
        
        # Fleet changes
        if 'fleet_changes' in actions:
            for change in actions['fleet_changes']:
                if change['action'] == 'add':
                    self.fleet.aircraft.append(Aircraft(**change['aircraft_data']))
                elif change['action'] == 'remove':
                    self.fleet.aircraft = [a for a in self.fleet.aircraft 
                                         if a.registration != change['registration']]
        
        # Financial changes
        if 'financial_changes' in actions:
            for change in actions['financial_changes']:
                if change['type'] == 'liability':
                    self.financial_model.update_liabilities(change['category'], change['amount'])
                elif change['type'] == 'asset':
                    self.financial_model.update_assets(change['category'], change['amount'])
    
    def _calculate_route_performance(self) -> Dict:
        """Calculate performance metrics for all routes."""
        performance = {
            'total_revenue': 0,
            'total_cost': 0,
            'route_details': {}
        }
        
        for route_key, route in self.route_network.routes.items():
            # Get appropriate aircraft for route
            aircraft = next((a for a in self.fleet.aircraft 
                           if a.type == route.aircraft_type and a.status == 'active'), None)
            
            if aircraft:
                revenue = route.calculate_revenue(aircraft.seating_capacity)
                cost = route.calculate_operating_cost(aircraft.seating_capacity)
                profit = revenue - cost
                
                performance['total_revenue'] += revenue
                performance['total_cost'] += cost
                
                performance['route_details'][route_key] = {
                    'revenue': revenue,
                    'cost': cost,
                    'profit': profit,
                    'load_factor': route.load_factor,
                    'break_even_load_factor': route.calculate_break_even_load_factor(
                        aircraft.seating_capacity
                    )
                }
        
        return performance
    
    def _update_financials(self, quarter: str, route_performance: Dict) -> FinancialMetrics:
        """Update financial metrics based on route performance."""
        return self.financial_model.calculate_quarterly_metrics(
            quarter=quarter,
            route_revenue=route_performance['total_revenue'],
            operating_costs=route_performance['total_cost'],
            fuel_costs=sum(route['cost'] * 0.3 for route in route_performance['route_details'].values()),
            maintenance_costs=self.fleet.calculate_total_maintenance_cost(),
            labor_costs=sum(route['cost'] * 0.25 for route in route_performance['route_details'].values()),
            airport_costs=sum(route['cost'] * 0.15 for route in route_performance['route_details'].values()),
            other_costs=sum(route['cost'] * 0.1 for route in route_performance['route_details'].values())
        )
    
    def _generate_quarterly_report(self, quarter: str, 
                                 route_performance: Dict,
                                 financial_metrics: FinancialMetrics) -> Dict:
        """Generate comprehensive quarterly report."""
        return {
            'quarter': quarter,
            'financial_summary': self.financial_model.get_financial_summary(quarter),
            'route_performance': route_performance,
            'fleet_status': {
                'total_aircraft': len(self.fleet.aircraft),
                'active_aircraft': len(self.fleet.get_available_aircraft()),
                'maintenance_aircraft': len(self.fleet.get_maintenance_aircraft()),
                'grounded_aircraft': len(self.fleet.get_grounded_aircraft()),
                'average_utilization': self.fleet.get_fleet_utilization()
            },
            'key_metrics': {
                'operating_margin': financial_metrics.operating_margin,
                'roic': self.financial_model.calculate_roic(quarter),
                'cash_burn_rate': self.financial_model.calculate_cash_burn_rate(quarter),
                'debt_to_equity': financial_metrics.debt_to_equity
            }
        }
    
    def run_simulation(self, quarters: int, actions_by_quarter: Dict[str, Dict]) -> List[Dict]:
        """Run simulation for multiple quarters."""
        reports = []
        current_date = datetime(2025, 1, 1)
        
        for i in range(quarters):
            quarter = f"{current_date.year}-Q{(i % 4) + 1}"
            actions = actions_by_quarter.get(quarter, {})
            
            report = self.run_quarter(quarter, actions)
            reports.append(report)
            
            # Save report to file
            with open(f'reports/{quarter}_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            current_date += timedelta(days=90)
        
        return reports

def main():
    """Main function to run the simulation."""
    # Create simulation instance
    simulation = BimanSimulation()
    
    # Define actions for each quarter
    actions = {
        '2025-Q1': {
            'route_changes': [
                {
                    'action': 'modify',
                    'origin': 'DAC',
                    'destination': 'NRT',
                    'modifications': {
                        'frequency': 0  # Suspend Narita route
                    }
                },
                {
                    'action': 'modify',
                    'origin': 'DAC',
                    'destination': 'MAN',
                    'modifications': {
                        'frequency': 2  # Reduce Manchester to twice weekly
                    }
                }
            ],
            'financial_changes': [
                {
                    'type': 'liability',
                    'category': 'aircraft_loans',
                    'amount': -50000000  # Reduce debt
                }
            ]
        }
    }
    
    # Run simulation for 4 quarters
    reports = simulation.run_simulation(4, actions)
    
    # Print summary of results
    for report in reports:
        print(f"\nQuarter: {report['quarter']}")
        print(f"Operating Margin: {report['key_metrics']['operating_margin']:.2f}%")
        print(f"ROIC: {report['key_metrics']['roic']:.2f}%")
        print(f"Cash Burn Rate: {report['key_metrics']['cash_burn_rate']:.2f}")

if __name__ == "__main__":
    main() 