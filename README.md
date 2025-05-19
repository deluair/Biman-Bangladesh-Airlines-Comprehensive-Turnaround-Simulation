# Biman Bangladesh Airlines Comprehensive Turnaround Simulation

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

This project provides a comprehensive, data-driven simulation and turnaround analysis for Biman Bangladesh Airlines. It models the airline's operational and financial challenges, simulates quarterly performance, and generates detailed reports and interactive dashboards to support strategic decision-making.

**Key objectives:**
- Model Biman's fleet, routes, and financials with realistic data
- Simulate quarterly operations and financial outcomes
- Analyze route profitability, fleet utilization, and key financial metrics
- Visualize results with static and interactive dashboards
- Support turnaround strategies based on data-driven insights

## Features

- **Aircraft, Fleet, and Route Modeling**: Realistic classes for aircraft, fleet, and route network
- **Financial Simulation**: Tracks operating margin, ROIC, cash burn, and more
- **Scenario Analysis**: Test different actions and turnaround strategies
- **Automated Reporting**: Generates quarterly JSON reports
- **Advanced Visualization**: Static plots and interactive dashboards (Plotly)
- **Statistical Analysis**: In-depth metrics, trends, and route comparisons
- **Export**: Analysis results in JSON, Excel, and CSV formats

## Project Structure

```
.
├── models/
│   ├── __init__.py
│   ├── aircraft.py
│   ├── fleet.py
│   ├── route.py
│   └── financial.py
├── reports/
│   └── ... (auto-generated quarterly reports)
├── visualizations/
│   ├── financial_metrics.png
│   ├── route_performance.png
│   ├── fleet_utilization.png
│   ├── summary_report.png
│   ├── dashboard.html
│   └── analysis_*.json|.xlsx|.csv
├── simulation.py
├── visualization.py
├── requirements.txt
└── README.md
```

## Data & Workflow

1. **Simulation** (`simulation.py`):
   - Models fleet, routes, and finances
   - Runs quarterly simulations
   - Outputs detailed JSON reports in `reports/`

2. **Visualization** (`visualization.py`):
   - Loads reports
   - Generates static plots and interactive dashboards in `visualizations/`
   - Performs advanced statistical analysis and exports results

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/deluair/Biman-Bangladesh-Airlines-Comprehensive-Turnaround-Simulation.git
   cd Biman-Bangladesh-Airlines-Comprehensive-Turnaround-Simulation
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### 1. Run the Simulation
Generates quarterly reports in `reports/`:
```sh
python simulation.py
```

### 2. Generate Visualizations & Analysis
Creates plots, dashboards, and exports in `visualizations/`:
```sh
python visualization.py
```

### 3. Explore Outputs
- **Static Plots:**
  - `visualizations/financial_metrics.png`
  - `visualizations/route_performance.png`
  - `visualizations/fleet_utilization.png`
  - `visualizations/summary_report.png`
- **Interactive Dashboard:**
  - `visualizations/dashboard.html` (open in your browser)
- **Statistical Analysis:**
  - `visualizations/analysis_*.json|.xlsx|.csv`

### 4. Example Output
> _Add screenshots or sample outputs here for quick reference._

## Modules

- `models/aircraft.py`: Aircraft properties and maintenance
- `models/fleet.py`: Fleet management and status
- `models/route.py`: Route network and profitability
- `models/financial.py`: Financial metrics and calculations
- `simulation.py`: Simulation engine and scenario runner
- `visualization.py`: Visualization, dashboard, and analytics

## Customization
- **Add new routes or aircraft**: Edit `models/route.py` or `models/aircraft.py`
- **Change scenarios**: Modify actions in `simulation.py`
- **Extend analytics**: Enhance `visualization.py` with new plots or metrics

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Citation
If you use this project for research or analysis, please cite appropriately.

---

For more details, see the [GitHub repository](https://github.com/deluair/Biman-Bangladesh-Airlines-Comprehensive-Turnaround-Simulation). 