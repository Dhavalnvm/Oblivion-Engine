# tests/test_optimization.py
"""
Tests for optimization components.
"""

import unittest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.optimization.solver import RailwaySolver


class TestOptimization(unittest.TestCase):
    """Test optimization solver functionality."""

    def setUp(self):
        self.solver = RailwaySolver(time_limit_ms=1000)
        self.platforms = ['P1', 'P2', 'P3']

    def test_simple_scheduling(self):
        """Test basic scheduling optimization."""
        # Create simple test data
        base_time = datetime.now()
        trains_data = pd.DataFrame({
            'train_id': ['T001', 'T002', 'T003'],
            'arrival_time': [
                base_time,
                base_time + timedelta(hours=1),
                base_time + timedelta(hours=2)
            ],
            'departure_time': [
                base_time + timedelta(minutes=30),
                base_time + timedelta(hours=1, minutes=30),
                base_time + timedelta(hours=2, minutes=30)
            ],
            'delay_minutes': [0, 5, 10]
        })

        result = self.solver.solve_scheduling(trains_data, self.platforms)

        # Check that solution exists
        self.assertIn('status', result)
        self.assertIn(result['status'], ['OPTIMAL', 'FEASIBLE'])

        # Check that all trains are assigned platforms
        assignments = result['platform_assignments']
        self.assertEqual(len(assignments), len(trains_data))

        for train_id in trains_data['train_id']:
            self.assertIn(train_id, assignments)
            self.assertIn(assignments[train_id], self.platforms)

    def test_conflicting_trains(self):
        """Test handling of time conflicts."""
        base_time = datetime.now()

        # Create overlapping trains
        trains_data = pd.DataFrame({
            'train_id': ['T001', 'T002'],
            'arrival_time': [base_time, base_time + timedelta(minutes=15)],
            'departure_time': [
                base_time + timedelta(minutes=30),
                base_time + timedelta(minutes=45)
            ],
            'delay_minutes': [0, 0]
        })

        # With only one platform, should be infeasible or require careful timing
        result = self.solver.solve_scheduling(trains_data, ['P1'])

        if result['status'] in ['OPTIMAL', 'FEASIBLE']:
            # If feasible, trains should have different platforms or non-overlapping times
            assignments = result['platform_assignments']
            self.assertEqual(len(set(assignments.values())), len(assignments))


if __name__ == '__main__':
    unittest.main()

