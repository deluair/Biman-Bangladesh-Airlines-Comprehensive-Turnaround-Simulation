import matplotlib.pyplot as plt
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional
import seaborn as sns
from scipy import stats
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from scipy.stats import shapiro, ttest_ind, f_oneway
import warnings
warnings.filterwarnings('ignore')

class SimulationVisualizer:
    """Visualizes simulation results and generates analysis plots."""
    
    def __init__(self, reports_dir: str = 'reports', update_interval: int = 300):
        self.reports_dir = Path(reports_dir)
        self.reports = self._load_reports()
        self.setup_style()
        self.update_interval = update_interval  # seconds
        self.last_update = datetime.now()
    
    def setup_style(self):
        """Set up consistent plotting style."""
        plt.style.use('seaborn-v0_8')  # Using a specific seaborn style version
        sns.set_palette("husl")
        pio.templates.default = "plotly_white"
    
    def _load_reports(self) -> List[Dict]:
        """Load all quarterly reports."""
        reports = []
        for report_file in sorted(self.reports_dir.glob('*_report.json')):
            with open(report_file, 'r') as f:
                reports.append(json.load(f))
        return reports
    
    def _check_for_updates(self) -> bool:
        """Check if reports need to be updated."""
        current_time = datetime.now()
        if (current_time - self.last_update).total_seconds() >= self.update_interval:
            self.reports = self._load_reports()
            self.last_update = current_time
            return True
        return False
    
    def plot_financial_metrics(self, save_path: str = None):
        """Plot key financial metrics over time."""
        quarters = [report['quarter'] for report in self.reports]
        metrics = {
            'Operating Margin (%)': [report['key_metrics']['operating_margin'] for report in self.reports],
            'ROIC (%)': [report['key_metrics']['roic'] for report in self.reports],
            'Cash Burn Rate': [report['key_metrics']['cash_burn_rate'] for report in self.reports]
        }
        
        df = pd.DataFrame(metrics, index=quarters)
        
        # Create figure with secondary y-axis
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Plot percentage metrics on primary y-axis
        ax1.plot(quarters, df['Operating Margin (%)'], 'b-', marker='o', label='Operating Margin (%)')
        ax1.plot(quarters, df['ROIC (%)'], 'g-', marker='s', label='ROIC (%)')
        ax1.set_xlabel('Quarter')
        ax1.set_ylabel('Percentage (%)')
        ax1.grid(True)
        
        # Create secondary y-axis for cash burn rate
        ax2 = ax1.twinx()
        ax2.plot(quarters, df['Cash Burn Rate'], 'r-', marker='^', label='Cash Burn Rate')
        ax2.set_ylabel('Cash Burn Rate')
        
        # Add legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.title('Financial Metrics Over Time')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    
    def plot_route_performance(self, save_path: str = None):
        """Plot route performance metrics."""
        route_data = []
        for report in self.reports:
            quarter = report['quarter']
            for route, metrics in report['route_performance']['route_details'].items():
                route_data.append({
                    'Quarter': quarter,
                    'Route': route,
                    'Profit': metrics['profit'],
                    'Load Factor': metrics['load_factor'] * 100,
                    'Break-even LF': metrics['break_even_load_factor'] * 100
                })
        
        df = pd.DataFrame(route_data)
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
        
        # Plot route profitability
        pivot_df = df.pivot(index='Quarter', columns='Route', values='Profit')
        pivot_df.plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_title('Route Profitability Over Time')
        ax1.set_xlabel('Quarter')
        ax1.set_ylabel('Profit')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True)
        
        # Plot load factors vs break-even
        for route in df['Route'].unique():
            route_df = df[df['Route'] == route]
            ax2.plot(route_df['Quarter'], route_df['Load Factor'], marker='o', label=f'{route} LF')
            ax2.plot(route_df['Quarter'], route_df['Break-even LF'], '--', label=f'{route} Break-even')
        
        ax2.set_title('Load Factors vs Break-even Points')
        ax2.set_xlabel('Quarter')
        ax2.set_ylabel('Load Factor (%)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    
    def plot_fleet_utilization(self, save_path: str = None):
        """Plot fleet utilization metrics."""
        quarters = [report['quarter'] for report in self.reports]
        fleet_status = {
            'Active': [report['fleet_status']['active_aircraft'] for report in self.reports],
            'Maintenance': [report['fleet_status']['maintenance_aircraft'] for report in self.reports],
            'Grounded': [report['fleet_status']['grounded_aircraft'] for report in self.reports]
        }
        
        df = pd.DataFrame(fleet_status, index=quarters)
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Stacked bar chart
        df.plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_title('Fleet Status Over Time')
        ax1.set_xlabel('Quarter')
        ax1.set_ylabel('Number of Aircraft')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True)
        
        # Utilization rate
        total_aircraft = df.sum(axis=1)
        utilization_rate = (df['Active'] / total_aircraft) * 100
        utilization_rate.plot(kind='line', marker='o', ax=ax2)
        ax2.set_title('Fleet Utilization Rate')
        ax2.set_xlabel('Quarter')
        ax2.set_ylabel('Utilization Rate (%)')
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    
    def perform_advanced_statistical_analysis(self) -> Dict:
        """Perform comprehensive statistical analysis on key metrics."""
        analysis = {}
        
        # Financial metrics analysis
        financial_data = {
            'Operating Margin': [report['key_metrics']['operating_margin'] for report in self.reports],
            'ROIC': [report['key_metrics']['roic'] for report in self.reports],
            'Cash Burn Rate': [report['key_metrics']['cash_burn_rate'] for report in self.reports]
        }
        
        for metric, values in financial_data.items():
            # Basic statistics
            analysis[metric] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'median': np.median(values),
                'iqr': stats.iqr(values),
                'skewness': stats.skew(values),
                'kurtosis': stats.kurtosis(values),
                'trend': np.polyfit(range(len(values)), values, 1)[0]
            }
            
            # Normality test
            _, p_value = shapiro(values)
            analysis[metric]['normality_test'] = {
                'p_value': p_value,
                'is_normal': p_value > 0.05
            }
            
            # Trend analysis
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            analysis[metric]['trend_analysis'] = {
                'slope': slope,
                'r_squared': r_value**2,
                'p_value': p_value,
                'std_err': std_err
            }
        
        # Route performance analysis
        route_data = []
        for report in self.reports:
            for route, metrics in report['route_performance']['route_details'].items():
                route_data.append({
                    'Route': route,
                    'Profit': metrics['profit'],
                    'Load Factor': metrics['load_factor'],
                    'Quarter': report['quarter']
                })
        
        df_routes = pd.DataFrame(route_data)
        
        # Route-specific analysis
        route_analysis = {}
        for route in df_routes['Route'].unique():
            route_df = df_routes[df_routes['Route'] == route]
            
            # Profitability analysis
            profit_stats = {
                'mean': route_df['Profit'].mean(),
                'std': route_df['Profit'].std(),
                'min': route_df['Profit'].min(),
                'max': route_df['Profit'].max(),
                'median': route_df['Profit'].median(),
                'profit_margin': (route_df['Profit'].sum() / len(route_df)) / route_df['Profit'].abs().max()
            }
            
            # Load factor analysis
            lf_stats = {
                'mean': route_df['Load Factor'].mean(),
                'std': route_df['Load Factor'].std(),
                'min': route_df['Load Factor'].min(),
                'max': route_df['Load Factor'].max(),
                'median': route_df['Load Factor'].median()
            }
            
            # Seasonality analysis
            quarterly_means = route_df.groupby('Quarter')['Load Factor'].mean()
            seasonality = {
                'q1_mean': quarterly_means.get('Q1', 0),
                'q2_mean': quarterly_means.get('Q2', 0),
                'q3_mean': quarterly_means.get('Q3', 0),
                'q4_mean': quarterly_means.get('Q4', 0)
            }
            
            route_analysis[route] = {
                'profitability': profit_stats,
                'load_factor': lf_stats,
                'seasonality': seasonality
            }
        
        analysis['Route Performance'] = route_analysis
        
        # Comparative analysis between routes
        route_comparison = {}
        routes = df_routes['Route'].unique()
        for i, route1 in enumerate(routes):
            for route2 in routes[i+1:]:
                route1_data = df_routes[df_routes['Route'] == route1]['Profit']
                route2_data = df_routes[df_routes['Route'] == route2]['Profit']
                
                # T-test for profit comparison
                t_stat, p_value = ttest_ind(route1_data, route2_data)
                route_comparison[f"{route1}_vs_{route2}"] = {
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'significant_difference': p_value < 0.05
                }
        
        analysis['Route Comparison'] = route_comparison
        
        return analysis
    
    def _to_native(self, obj):
        """Recursively convert numpy types to native Python types."""
        if isinstance(obj, dict):
            return {self._to_native(k): self._to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._to_native(i) for i in obj]
        elif isinstance(obj, np.generic):
            return obj.item()
        else:
            return obj

    def export_analysis(self, analysis: Dict, format: str = 'json') -> str:
        """Export analysis results in various formats."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format.lower() == 'json':
            output_path = f'analysis_{timestamp}.json'
            with open(output_path, 'w') as f:
                json.dump(self._to_native(analysis), f, indent=4)
        
        elif format.lower() == 'excel':
            output_path = f'analysis_{timestamp}.xlsx'
            with pd.ExcelWriter(output_path) as writer:
                # Financial metrics
                financial_df = pd.DataFrame(analysis).T
                financial_df.to_excel(writer, sheet_name='Financial Metrics')
                
                # Route performance
                route_perf = analysis['Route Performance']
                route_df = pd.DataFrame.from_dict(route_perf, orient='index')
                route_df.to_excel(writer, sheet_name='Route Performance')
                
                # Route comparison
                comp_df = pd.DataFrame.from_dict(analysis['Route Comparison'], orient='index')
                comp_df.to_excel(writer, sheet_name='Route Comparison')
        
        elif format.lower() == 'csv':
            output_path = f'analysis_{timestamp}.csv'
            # Flatten nested dictionary for CSV export
            flat_analysis = {}
            for key, value in analysis.items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        flat_analysis[f"{key}_{subkey}"] = subvalue
                else:
                    flat_analysis[key] = value
            
            pd.DataFrame.from_dict(self._to_native(flat_analysis), orient='index').to_csv(output_path)
        
        return output_path
    
    def generate_interactive_dashboard(self, save_path: str = None):
        """Generate an interactive dashboard using Plotly."""
        # Check for updates
        self._check_for_updates()
        
        # Create subplot figure with more detailed layout
        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=(
                'Financial Performance', 'Route Profitability',
                'Fleet Status', 'Load Factors',
                'Cash Flow Analysis', 'Route Network Map',
                'Statistical Analysis', 'Performance Trends'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "table"}, {"type": "scatter"}]
            ]
        )
        
        # Financial metrics with confidence intervals
        quarters = [report['quarter'] for report in self.reports]
        metrics = {
            'Operating Margin (%)': [report['key_metrics']['operating_margin'] for report in self.reports],
            'ROIC (%)': [report['key_metrics']['roic'] for report in self.reports]
        }
        
        for metric, values in metrics.items():
            # Calculate confidence intervals
            mean = np.mean(values)
            std = np.std(values)
            ci = 1.96 * std / np.sqrt(len(values))
            
            fig.add_trace(
                go.Scatter(
                    x=quarters,
                    y=values,
                    name=metric,
                    mode='lines+markers',
                    error_y=dict(type='data', array=[ci]*len(values), visible=True)
                ),
                row=1, col=1
            )
        
        # Route performance with statistical annotations
        route_data = []
        for report in self.reports:
            quarter = report['quarter']
            for route, metrics in report['route_performance']['route_details'].items():
                route_data.append({
                    'Quarter': quarter,
                    'Route': route,
                    'Profit': metrics['profit']
                })
        
        df_routes = pd.DataFrame(route_data)
        pivot_routes = df_routes.pivot(index='Quarter', columns='Route', values='Profit')
        
        for route in pivot_routes.columns:
            fig.add_trace(
                go.Bar(
                    x=pivot_routes.index,
                    y=pivot_routes[route],
                    name=route,
                    text=pivot_routes[route].round(2),
                    textposition='auto'
                ),
                row=1, col=2
            )
        
        # Fleet status with utilization rate
        fleet_status = {
            'Active': [report['fleet_status']['active_aircraft'] for report in self.reports],
            'Maintenance': [report['fleet_status']['maintenance_aircraft'] for report in self.reports],
            'Grounded': [report['fleet_status']['grounded_aircraft'] for report in self.reports]
        }
        
        for status, values in fleet_status.items():
            fig.add_trace(
                go.Bar(
                    x=quarters,
                    y=values,
                    name=status,
                    text=values,
                    textposition='auto'
                ),
                row=2, col=1
            )
        
        # Load factors with break-even lines
        load_factors = []
        for report in self.reports:
            quarter = report['quarter']
            for route, metrics in report['route_performance']['route_details'].items():
                load_factors.append({
                    'Quarter': quarter,
                    'Route': route,
                    'Load Factor': metrics['load_factor'] * 100,
                    'Break-even LF': metrics['break_even_load_factor'] * 100
                })
        
        df_load = pd.DataFrame(load_factors)
        pivot_load = df_load.pivot(index='Quarter', columns='Route', values='Load Factor')
        pivot_break_even = df_load.pivot(index='Quarter', columns='Route', values='Break-even LF')
        
        for route in pivot_load.columns:
            fig.add_trace(
                go.Scatter(
                    x=pivot_load.index,
                    y=pivot_load[route],
                    name=f'{route} LF',
                    mode='lines+markers'
                ),
                row=2, col=2
            )
            fig.add_trace(
                go.Scatter(
                    x=pivot_break_even.index,
                    y=pivot_break_even[route],
                    name=f'{route} Break-even',
                    mode='lines',
                    line=dict(dash='dash')
                ),
                row=2, col=2
            )
        
        # Statistical analysis table
        analysis = self.perform_advanced_statistical_analysis()
        stats_table = pd.DataFrame(analysis).round(4)
        fig.add_trace(
            go.Table(
                header=dict(values=list(stats_table.columns)),
                cells=dict(values=[stats_table[col] for col in stats_table.columns])
            ),
            row=4, col=1
        )
        
        # Update layout with more interactive features
        fig.update_layout(
            height=1600,
            width=1800,
            title_text="Biman Bangladesh Airlines Performance Dashboard",
            showlegend=True,
            hovermode='x unified',
            template='plotly_white',
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    x=0.7,
                    y=1.2,
                    showactive=True,
                    buttons=list([
                        dict(
                            args=[{"visible": [True] * len(fig.data)}],
                            label="Show All",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [True if (trace.name and "LF" in trace.name) else False for trace in fig.data]}],
                            label="Load Factors Only",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [True if (trace.name and "Profit" in trace.name) else False for trace in fig.data]}],
                            label="Profitability Only",
                            method="update"
                        )
                    ])
                )
            ]
        )
        
        if save_path:
            fig.write_html(save_path, include_plotlyjs='cdn')
    
    def generate_summary_report(self, save_path: str = None):
        """Generate a comprehensive summary report with multiple visualizations."""
        # Check for updates
        self._check_for_updates()
        
        # Create subplots with enhanced layout
        fig = plt.figure(figsize=(20, 15))
        gs = fig.add_gridspec(4, 2)
        
        # Financial metrics with confidence intervals
        ax1 = fig.add_subplot(gs[0, 0])
        quarters = [report['quarter'] for report in self.reports]
        metrics = {
            'Operating Margin (%)': [report['key_metrics']['operating_margin'] for report in self.reports],
            'ROIC (%)': [report['key_metrics']['roic'] for report in self.reports]
        }
        
        for metric, values in metrics.items():
            mean = np.mean(values)
            std = np.std(values)
            ci = 1.96 * std / np.sqrt(len(values))
            ax1.plot(quarters, values, marker='o', label=metric)
            ax1.fill_between(quarters, 
                           [v - ci for v in values],
                           [v + ci for v in values],
                           alpha=0.2)
        
        ax1.set_title('Financial Performance with Confidence Intervals')
        ax1.grid(True)
        ax1.legend()
        
        # Route performance with statistical annotations
        ax2 = fig.add_subplot(gs[0, 1])
        route_data = []
        for report in self.reports:
            quarter = report['quarter']
            for route, metrics in report['route_performance']['route_details'].items():
                route_data.append({
                    'Quarter': quarter,
                    'Route': route,
                    'Profit': metrics['profit']
                })
        
        df_routes = pd.DataFrame(route_data)
        pivot_routes = df_routes.pivot(index='Quarter', columns='Route', values='Profit')
        pivot_routes.plot(kind='bar', stacked=True, ax=ax2)
        ax2.set_title('Route Profitability')
        ax2.grid(True)
        
        # Fleet utilization with trend line
        ax3 = fig.add_subplot(gs[1, :])
        fleet_status = {
            'Active': [report['fleet_status']['active_aircraft'] for report in self.reports],
            'Maintenance': [report['fleet_status']['maintenance_aircraft'] for report in self.reports],
            'Grounded': [report['fleet_status']['grounded_aircraft'] for report in self.reports]
        }
        df_fleet = pd.DataFrame(fleet_status, index=quarters)
        df_fleet.plot(kind='bar', stacked=True, ax=ax3)
        
        # Add trend line for active aircraft
        z = np.polyfit(range(len(quarters)), df_fleet['Active'], 1)
        p = np.poly1d(z)
        ax3.plot(range(len(quarters)), p(range(len(quarters))), "r--", alpha=0.8)
        
        ax3.set_title('Fleet Status with Utilization Trend')
        ax3.grid(True)
        
        # Load factors with break-even points
        ax4 = fig.add_subplot(gs[2, :])
        load_factors = []
        for report in self.reports:
            quarter = report['quarter']
            for route, metrics in report['route_performance']['route_details'].items():
                load_factors.append({
                    'Quarter': quarter,
                    'Route': route,
                    'Load Factor': metrics['load_factor'] * 100,
                    'Break-even LF': metrics['break_even_load_factor'] * 100
                })
        
        df_load = pd.DataFrame(load_factors)
        for route in df_load['Route'].unique():
            route_df = df_load[df_load['Route'] == route]
            ax4.plot(route_df['Quarter'], route_df['Load Factor'], 
                    marker='o', label=f'{route} LF')
            ax4.plot(route_df['Quarter'], route_df['Break-even LF'], 
                    '--', label=f'{route} Break-even')
        
        ax4.set_title('Load Factors vs Break-even Points')
        ax4.grid(True)
        ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Statistical summary
        ax5 = fig.add_subplot(gs[3, :])
        analysis = self.perform_advanced_statistical_analysis()
        stats_text = "Statistical Summary:\n\n"
        for metric, stats in analysis.items():
            if isinstance(stats, dict) and 'mean' in stats:
                stats_text += f"{metric}:\n"
                stats_text += f"Mean: {stats['mean']:.2f}\n"
                stats_text += f"Std: {stats['std']:.2f}\n"
                stats_text += f"Trend: {stats['trend']:.2f}\n\n"
        
        ax5.text(0.1, 0.5, stats_text, fontsize=10, va='center')
        ax5.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()

def main():
    """Generate visualization reports."""
    visualizer = SimulationVisualizer()
    
    # Create visualizations directory
    viz_dir = Path('visualizations')
    viz_dir.mkdir(exist_ok=True)
    
    # Generate individual plots
    visualizer.plot_financial_metrics(viz_dir / 'financial_metrics.png')
    visualizer.plot_route_performance(viz_dir / 'route_performance.png')
    visualizer.plot_fleet_utilization(viz_dir / 'fleet_utilization.png')
    
    # Generate comprehensive summary
    visualizer.generate_summary_report(viz_dir / 'summary_report.png')
    
    # Generate interactive dashboard
    visualizer.generate_interactive_dashboard(viz_dir / 'dashboard.html')
    
    # Perform statistical analysis and export
    analysis = visualizer.perform_advanced_statistical_analysis()
    visualizer.export_analysis(analysis, 'json')
    visualizer.export_analysis(analysis, 'excel')
    visualizer.export_analysis(analysis, 'csv')

if __name__ == "__main__":
    main() 