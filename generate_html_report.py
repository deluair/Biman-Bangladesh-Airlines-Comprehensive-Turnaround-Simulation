import os
import json
import base64
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Paths
VIS_DIR = Path('visualizations')
REPORTS_DIR = Path('reports')

# Helper to encode images as base64 data URIs
def img_to_base64(path):
    with open(path, 'rb') as img_f:
        encoded = base64.b64encode(img_f.read()).decode('utf-8')
    ext = os.path.splitext(path)[1][1:]
    return f"data:image/{ext};base64,{encoded}"

# Load key images as base64
images = {}
for key, rel_path in {
    'financial_metrics': 'visualizations/financial_metrics.png',
    'route_performance': 'visualizations/route_performance.png',
    'fleet_utilization': 'visualizations/fleet_utilization.png',
    'summary_report': 'visualizations/summary_report.png',
}.items():
    if Path(rel_path).exists():
        images[key] = img_to_base64(rel_path)
    else:
        images[key] = ''

# Load analysis (latest JSON)
analysis_files = sorted(VIS_DIR.glob('analysis_*.json'), reverse=True)
analysis = {}
if analysis_files:
    with open(analysis_files[0], 'r') as f:
        analysis = json.load(f)

# Load a sample report (latest quarter)
report_files = sorted(REPORTS_DIR.glob('*_report.json'), reverse=True)
sample_report = {}
if report_files:
    with open(report_files[0], 'r') as f:
        sample_report = json.load(f)

# Prepare tables
key_metrics = sample_report.get('key_metrics', {})
route_details = sample_report.get('route_performance', {}).get('route_details', {})
fleet_status = sample_report.get('fleet_status', {})

# Prepare route table
route_table = []
for route, metrics in route_details.items():
    row = {'Route': route}
    row.update(metrics)
    route_table.append(row)
route_df = pd.DataFrame(route_table)

# Format numbers in route_df
numeric_columns = ['revenue', 'cost', 'profit', 'load_factor', 'break_even_load_factor']
for col in numeric_columns:
    if col in route_df.columns:
        route_df[col] = route_df[col].apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)

# Prepare fleet table
fleet_df = pd.DataFrame([fleet_status])

# Format numbers in fleet_df
numeric_columns = ['total_aircraft', 'active_aircraft', 'maintenance_aircraft', 'grounded_aircraft', 'average_utilization']
for col in numeric_columns:
    if col in fleet_df.columns:
        fleet_df[col] = fleet_df[col].apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)

# Jinja2 template setup
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template_str = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biman Bangladesh Airlines Turnaround Simulation Report</title>
    <style>
        :root {
            --primary-color: #003366;
            --secondary-color: #0066cc;
            --accent-color: #ff9900;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --warning-color: #ffc107;
            --light-bg: #f8f9fa;
            --dark-bg: #343a40;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: var(--light-bg);
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: var(--primary-color);
            color: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        h1, h2, h3 {
            color: var(--primary-color);
            margin-top: 0;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        
        h2 {
            font-size: 1.8em;
            margin-bottom: 15px;
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 10px;
        }
        
        h3 {
            font-size: 1.4em;
            margin-bottom: 10px;
            color: var(--secondary-color);
        }
        
        .section {
            margin-bottom: 40px;
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        img {
            max-width: 100%;
            border: 1px solid #ccc;
            margin: 20px 0;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background: var(--primary-color);
            color: white;
            font-weight: 500;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tr:hover {
            background-color: #f1f1f1;
        }
        
        .profit-positive {
            color: var(--success-color);
            font-weight: bold;
        }
        
        .profit-negative {
            color: var(--danger-color);
            font-weight: bold;
        }
        
        .footer {
            color: #666;
            font-size: 0.9em;
            margin-top: 40px;
            text-align: center;
            padding: 20px;
            border-top: 1px solid #ddd;
        }
        
        .footer a {
            color: var(--secondary-color);
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .section {
                padding: 15px;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Biman Bangladesh Airlines<br>Comprehensive Turnaround Simulation</h1>
        </div>
        
        <div class="section">
            <h2>Executive Summary</h2>
            <p>This report presents a detailed simulation and turnaround analysis for Biman Bangladesh Airlines, including operational, financial, and route-level insights. All visuals and tables are generated from the latest simulation run.</p>
        </div>
        
        <div class="section">
            <h2>Key Financial Metrics</h2>
            <div class="metrics-grid">
                {% for k, v in key_metrics.items() %}
                <div class="metric-card">
                    <div class="metric-value">{{ "%.2f"|format(v) }}</div>
                    <div class="metric-label">{{ k.replace('_', ' ').title() }}</div>
                </div>
                {% endfor %}
            </div>
            <img src="{{ images['financial_metrics'] }}" alt="Financial Metrics Plot">
        </div>
        
        <div class="section">
            <h2>Route Performance</h2>
            <img src="{{ images['route_performance'] }}" alt="Route Performance Plot">
            <h3>Route Details (Latest Quarter)</h3>
            <div style="overflow-x: auto;">
                {{ route_df.to_html(index=False, classes='route-table') | safe }}
            </div>
        </div>
        
        <div class="section">
            <h2>Fleet Utilization</h2>
            <img src="{{ images['fleet_utilization'] }}" alt="Fleet Utilization Plot">
            <h3>Fleet Status (Latest Quarter)</h3>
            <div style="overflow-x: auto;">
                {{ fleet_df.to_html(index=False, classes='fleet-table') | safe }}
            </div>
        </div>
        
        <div class="section">
            <h2>Comprehensive Summary</h2>
            <img src="{{ images['summary_report'] }}" alt="Summary Report Plot">
        </div>
        
        <div class="section">
            <h2>Statistical Analysis</h2>
            <pre>{{ analysis | tojson(indent=2) }}</pre>
        </div>
        
        <div class="footer">
            <p>Generated by Biman Bangladesh Airlines Turnaround Simulation &copy; 2025</p>
            <p>For more information, visit our <a href="https://github.com/deluair/Biman-Bangladesh-Airlines-Comprehensive-Turnaround-Simulation">project repository</a></p>
        </div>
    </div>
</body>
</html>
'''

template = env.from_string(template_str)

# Render HTML
html = template.render(
    key_metrics=key_metrics,
    images=images,
    route_df=route_df,
    fleet_df=fleet_df,
    analysis=analysis
)

# Output file
output_path = VIS_DIR / 'detailed_report.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Detailed HTML report generated: {output_path}") 