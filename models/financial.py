from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal

@dataclass
class FinancialMetrics:
    """Represents key financial metrics for the airline."""
    revenue: float
    operating_cost: float
    fuel_cost: float
    maintenance_cost: float
    labor_cost: float
    airport_charges: float
    other_costs: float
    ebitda: float
    net_income: float
    cash_balance: float
    total_debt: float
    total_assets: float
    
    @property
    def operating_margin(self) -> float:
        """Calculate operating margin."""
        if self.revenue == 0:
            return 0.0
        return (self.ebitda / self.revenue) * 100
    
    @property
    def debt_to_equity(self) -> float:
        """Calculate debt-to-equity ratio."""
        equity = self.total_assets - self.total_debt
        if equity == 0:
            return float('inf')
        return self.total_debt / equity

class FinancialModel:
    """Manages the financial aspects of Biman Bangladesh Airlines."""
    
    def __init__(self):
        self.metrics: Dict[str, FinancialMetrics] = {}
        self.liabilities: Dict[str, float] = {
            'aircraft_loans': 1040000000,  # $1.04 billion
            'fuel_payments': 970000000,    # Tk 9.70 billion
            'employee_benefits': 1075000000,  # Tk 10.75 billion
            'airport_charges': 3866000000,  # Tk 38.66 billion
        }
        self.assets: Dict[str, float] = {
            'aircraft': 2500000000,  # Estimated value of fleet
            'cash': 50000000,        # Initial cash balance
            'other_assets': 100000000
        }
        self.initialize_financials()
    
    def initialize_financials(self):
        """Initialize financial data with realistic starting values."""
        # Initial metrics for Q1 2025
        self.metrics['2025-Q1'] = FinancialMetrics(
            revenue=500000000,  # Tk 500 million
            operating_cost=450000000,
            fuel_cost=150000000,
            maintenance_cost=80000000,
            labor_cost=120000000,
            airport_charges=50000000,
            other_costs=50000000,
            ebitda=50000000,
            net_income=20000000,
            cash_balance=50000000,
            total_debt=sum(self.liabilities.values()),
            total_assets=sum(self.assets.values())
        )
    
    def calculate_quarterly_metrics(self, quarter: str, 
                                  route_revenue: float,
                                  operating_costs: float,
                                  fuel_costs: float,
                                  maintenance_costs: float,
                                  labor_costs: float,
                                  airport_costs: float,
                                  other_costs: float) -> FinancialMetrics:
        """Calculate financial metrics for a given quarter."""
        revenue = route_revenue
        operating_cost = operating_costs
        ebitda = revenue - operating_cost
        
        # Calculate interest expense (assuming 5% annual rate)
        interest_expense = (self.liabilities['aircraft_loans'] * 0.05) / 4
        
        # Calculate depreciation (assuming 20-year life for aircraft)
        depreciation = (self.assets['aircraft'] / 20) / 4
        
        # Calculate net income
        net_income = ebitda - interest_expense - depreciation
        
        # Update cash balance
        self.assets['cash'] += net_income
        
        # Create and store metrics
        metrics = FinancialMetrics(
            revenue=revenue,
            operating_cost=operating_cost,
            fuel_cost=fuel_costs,
            maintenance_cost=maintenance_costs,
            labor_cost=labor_costs,
            airport_charges=airport_costs,
            other_costs=other_costs,
            ebitda=ebitda,
            net_income=net_income,
            cash_balance=self.assets['cash'],
            total_debt=sum(self.liabilities.values()),
            total_assets=sum(self.assets.values())
        )
        
        self.metrics[quarter] = metrics
        return metrics
    
    def get_quarterly_metrics(self, quarter: str) -> Optional[FinancialMetrics]:
        """Get financial metrics for a specific quarter."""
        return self.metrics.get(quarter)
    
    def calculate_roic(self, quarter: str) -> float:
        """Calculate Return on Invested Capital for a quarter."""
        metrics = self.get_quarterly_metrics(quarter)
        if not metrics:
            return 0.0
        
        invested_capital = metrics.total_assets - metrics.total_debt
        if invested_capital == 0:
            return 0.0
        
        return (metrics.net_income / invested_capital) * 100
    
    def calculate_cash_burn_rate(self, quarter: str) -> float:
        """Calculate cash burn rate for a quarter."""
        metrics = self.get_quarterly_metrics(quarter)
        if not metrics:
            return 0.0
        
        return metrics.net_income / 90  # Daily cash burn rate
    
    def update_liabilities(self, liability_type: str, amount: float):
        """Update a specific liability."""
        if liability_type in self.liabilities:
            self.liabilities[liability_type] += amount
    
    def update_assets(self, asset_type: str, amount: float):
        """Update a specific asset."""
        if asset_type in self.assets:
            self.assets[asset_type] += amount
    
    def get_financial_summary(self, quarter: str) -> Dict[str, float]:
        """Get a summary of key financial metrics for a quarter."""
        metrics = self.get_quarterly_metrics(quarter)
        if not metrics:
            return {}
        
        return {
            'revenue': metrics.revenue,
            'operating_cost': metrics.operating_cost,
            'ebitda': metrics.ebitda,
            'net_income': metrics.net_income,
            'operating_margin': metrics.operating_margin,
            'debt_to_equity': metrics.debt_to_equity,
            'roic': self.calculate_roic(quarter),
            'cash_burn_rate': self.calculate_cash_burn_rate(quarter)
        } 