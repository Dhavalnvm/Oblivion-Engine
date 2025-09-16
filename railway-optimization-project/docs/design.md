# System Design

## Data Flow
1. Mock data generation simulates real train arrivals/departures
2. CP-SAT solver optimizes platform assignments and scheduling
3. PyQt dashboard displays results and allows user interaction

## Optimization Model
- Variables: Platform assignments for each train
- Constraints: 
  - No platform conflicts (time overlap)
  - Train capacity limits
  - Platform availability
- Objective: Minimize total delays

## UI Components
- Train Schedule Table: Shows current and optimized schedules
- Optimization Controls: Run solver, configure parameters
- Status Display: Solver results and timing information