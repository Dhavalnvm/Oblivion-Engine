# Railway Optimization Prototype

A minimal PyQt-based railway optimization engine prototype that demonstrates:
- Mock train data generation
- CP-SAT constraint optimization
- Real-time dashboard visualization

## Features

- **Mock Data Simulation**: Generates realistic train schedules, delays, and platform assignments
- **CP-SAT Optimization**: Uses Google OR-Tools to optimize train scheduling with constraints
- **PyQt Dashboard**: Interactive UI showing train data and optimization results
- **Configurable Settings**: YAML-based configuration for easy customization

## Quick Start

1. Install dependencies:
   ```bash
   pip install PyQt5 ortools pyyaml pandas numpy
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Use the dashboard to:
   - View current train schedules
   - Run optimization to minimize delays
   - See optimized platform assignments

## Architecture

- `mock_data.py`: Generates simulated train data
- `optimization.py`: CP-SAT solver for scheduling optimization
- `main_window.py`: PyQt main application window
- `dashboard.py`: Dashboard tab implementation
- `settings.yaml`: Configuration parameters

## Note

This is a prototype version. The full system would include:
- Real-time data pipelines (Kafka, Redis)
- Machine learning predictions
- Digital twin integration
- Multi-station optimization
- Advanced constraint handling
