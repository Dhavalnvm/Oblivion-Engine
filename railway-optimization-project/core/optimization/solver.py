# core/optimization/solver.py
"""
CP-SAT solver implementation for railway optimization.
"""

from ortools.sat.python import cp_model
import pandas as pd
from datetime import datetime, timedelta
import logging


class RailwaySolver:
    """CP-SAT solver for train scheduling optimization."""

    def __init__(self, time_limit_ms=5000):
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = time_limit_ms / 1000
        self.logger = logging.getLogger(__name__)

    def solve_scheduling(self, trains_df, platforms):
        """
        Solve train scheduling optimization problem.

        Args:
            trains_df: DataFrame with train data
            platforms: List of available platforms

        Returns:
            dict: Optimization results
        """
        self.logger.info("Starting optimization...")

        # Create model
        self.model = cp_model.CpModel()

        # Variables: platform assignment for each train
        platform_vars = {}
        for _, train in trains_df.iterrows():
            train_id = train['train_id']
            platform_vars[train_id] = {}
            for platform in platforms:
                platform_vars[train_id][platform] = self.model.NewBoolVar(
                    f'train_{train_id}_platform_{platform}'
                )

        # Constraint: Each train must be assigned exactly one platform
        for train_id in platform_vars:
            self.model.Add(
                sum(platform_vars[train_id][p] for p in platforms) == 1
            )

        # Constraint: No platform conflicts (time overlap)
        self._add_time_constraints(trains_df, platforms, platform_vars)

        # Objective: Minimize delays (simplified)
        delay_vars = []
        for _, train in trains_df.iterrows():
            if 'delay_minutes' in train:
                delay_vars.append(train['delay_minutes'])

        if delay_vars:
            self.model.Minimize(sum(delay_vars))

        # Solve
        status = self.solver.Solve(self.model)

        return self._extract_solution(status, trains_df, platforms, platform_vars)

    def _add_time_constraints(self, trains_df, platforms, platform_vars):
        """Add time-based constraints to prevent platform conflicts."""
        trains_list = trains_df.to_dict('records')

        for i, train1 in enumerate(trains_list):
            for j, train2 in enumerate(trains_list[i + 1:], i + 1):
                for platform in platforms:
                    # Check if trains overlap in time
                    if self._times_overlap(train1, train2):
                        # They cannot both use the same platform
                        self.model.Add(
                            platform_vars[train1['train_id']][platform] +
                            platform_vars[train2['train_id']][platform] <= 1
                        )

    def _times_overlap(self, train1, train2):
        """Check if two trains have overlapping platform usage times."""
        try:
            arr1 = pd.to_datetime(train1['arrival_time'])
            dep1 = pd.to_datetime(train1['departure_time'])
            arr2 = pd.to_datetime(train2['arrival_time'])
            dep2 = pd.to_datetime(train2['departure_time'])

            # Add buffer time for platform switching
            buffer = timedelta(minutes=5)

            return not (dep1 + buffer <= arr2 or dep2 + buffer <= arr1)
        except:
            return False

    def _extract_solution(self, status, trains_df, platforms, platform_vars):
        """Extract solution from solved model."""
        result = {
            'status': self._get_status_name(status),
            'solve_time': self.solver.WallTime(),
            'platform_assignments': {},
            'objective_value': None
        }

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # Extract platform assignments
            for train_id in platform_vars:
                for platform in platforms:
                    if self.solver.Value(platform_vars[train_id][platform]):
                        result['platform_assignments'][train_id] = platform
                        break

            result['objective_value'] = self.solver.ObjectiveValue()
            self.logger.info(f"Optimization completed: {result['status']}")
        else:
            self.logger.warning(f"Optimization failed: {result['status']}")

        return result

    def _get_status_name(self, status):
        """Convert status code to readable name."""
        status_names = {
            cp_model.OPTIMAL: 'OPTIMAL',
            cp_model.FEASIBLE: 'FEASIBLE',
            cp_model.INFEASIBLE: 'INFEASIBLE',
            cp_model.UNKNOWN: 'UNKNOWN',
            cp_model.MODEL_INVALID: 'MODEL_INVALID'
        }
        return status_names.get(status, 'UNKNOWN')

