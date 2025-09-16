# =============================================================================
# optimization.py - Simple Optimization Module
# =============================================================================
"""
Simple optimization module for railway scheduling.
"""

import pandas as pd
from datetime import datetime, timedelta
import logging
import random


def generate_mock_trains(num_trains=10):
    """Generate mock train data."""
    base_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    platforms = ['P1', 'P2', 'P3', 'P4', 'P5']

    trains_data = []
    for i in range(num_trains):
        train_id = f"T{i + 1:03d}"
        arrival_time = base_time + timedelta(hours=i * 0.5, minutes=random.randint(0, 30))
        departure_time = arrival_time + timedelta(minutes=random.randint(15, 45))
        delay = random.randint(0, 15)

        trains_data.append({
            'train_id': train_id,
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'platform': random.choice(platforms + [None]),
            'delay_minutes': delay
        })

    return pd.DataFrame(trains_data)


def simple_platform_assignment(trains_df, platforms=['P1', 'P2', 'P3', 'P4', 'P5']):
    """Simple platform assignment algorithm."""
    assignments = {}

    for i, (_, train) in enumerate(trains_df.iterrows()):
        # Round-robin assignment
        platform = platforms[i % len(platforms)]
        assignments[train['train_id']] = platform

    return assignments


def run_optimization(num_trains=10):
    """Run simple optimization workflow."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting simple optimization...")

    try:
        # Generate data
        trains_df = generate_mock_trains(num_trains)
        logger.info(f"Generated {len(trains_df)} trains")

        # Run assignment
        assignments = simple_platform_assignment(trains_df)

        result = {
            'status': 'SUCCESS',
            'assignments': assignments,
            'num_trains': len(trains_df),
            'solve_time': 0.1  # Simulated solve time
        }

        logger.info("Optimization completed successfully")
        return result

    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        return {
            'status': 'ERROR',
            'error': str(e),
            'assignments': {}
        }


def print_optimization_results(result):
    """Print optimization results."""
    print("\n" + "=" * 50)
    print("RAILWAY OPTIMIZATION RESULTS")
    print("=" * 50)

    print(f"Status: {result['status']}")
    if 'solve_time' in result:
        print(f"Solve Time: {result['solve_time']:.2f} seconds")

    assignments = result.get('assignments', {})
    if assignments:
        print(f"\nPlatform Assignments ({len(assignments)} trains):")
        print("-" * 30)

        platform_groups = {}
        for train_id, platform in assignments.items():
            if platform not in platform_groups:
                platform_groups[platform] = []
            platform_groups[platform].append(train_id)

        for platform in sorted(platform_groups.keys()):
            trains = platform_groups[platform]
            print(f"{platform}: {', '.join(trains)} ({len(trains)} trains)")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    result = run_optimization()
    print_optimization_results(result)