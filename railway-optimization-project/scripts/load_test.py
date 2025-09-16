# scripts/load_test.py
"""
Load testing script for railway optimization.
"""

import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.optimization.solver import RailwaySolver
from mock_data import generate_mock_trains


def run_load_test(num_trains_list=[10, 50, 100, 200], platforms=['P1', 'P2', 'P3', 'P4', 'P5']):
    """Run load test with varying numbers of trains."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    results = []

    for num_trains in num_trains_list:
        logger.info(f"Testing with {num_trains} trains...")

        # Generate test data
        trains_df = generate_mock_trains(num_trains)

        # Run optimization
        solver = RailwaySolver(time_limit_ms=10000)  # 10 second limit

        start_time = time.time()
        result = solver.solve_scheduling(trains_df, platforms)
        end_time = time.time()

        # Record results
        test_result = {
            'num_trains': num_trains,
            'status': result['status'],
            'solve_time_ms': result['solve_time'],
            'wall_time_s': end_time - start_time,
            'feasible': result['status'] in ['OPTIMAL', 'FEASIBLE'],
            'assignments_count': len(result['platform_assignments'])
        }

        results.append(test_result)
        logger.info(f"Result: {test_result}")

    # Summary
    logger.info("Load test summary:")
    for result in results:
        logger.info(f"  {result['num_trains']} trains: {result['status']} in {result['wall_time_s']:.2f}s")

    return results


if __name__ == "__main__":
    run_load_test()

