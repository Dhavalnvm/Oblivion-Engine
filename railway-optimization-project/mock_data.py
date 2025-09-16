# mock_data.py
"""
Mock data generation for railway optimization prototype.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import yaml


def load_settings():
    """Load settings from configuration file."""
    try:
        with open('config/settings.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Return default settings if config file doesn't exist
        return {
            'simulation': {
                'num_trains': 15,
                'station_code': 'NDLS',
                'platforms': ['P1', 'P2', 'P3', 'P4', 'P5'],
                'time_window_hours': 8
            }
        }


def generate_mock_trains(num_trains=None):
    """
    Generate mock train data for testing and demonstration.

    Args:
        num_trains: Number of trains to generate (overrides config)

    Returns:
        pandas.DataFrame: Mock train schedule data
    """
    settings = load_settings()

    if num_trains is None:
        num_trains = settings['simulation']['num_trains']

    platforms = settings['simulation']['platforms']
    time_window_hours = settings['simulation']['time_window_hours']

    # Base time for scheduling
    base_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)

    trains_data = []

    for i in range(num_trains):
        train_id = f"T{i + 1:03d}"

        # Random arrival time within the time window
        arrival_offset = timedelta(
            hours=random.uniform(0, time_window_hours),
            minutes=random.randint(0, 59)
        )
        arrival_time = base_time + arrival_offset

        # Departure time (15-45 minutes after arrival)
        departure_offset = timedelta(minutes=random.randint(15, 45))
        departure_time = arrival_time + departure_offset

        # Random delay (0-20 minutes, exponential distribution)
        delay_minutes = int(np.random.exponential(3))
        delay_minutes = min(delay_minutes, 20)  # Cap at 20 minutes

        # Adjust times for delay
        if delay_minutes > 0:
            arrival_time += timedelta(minutes=delay_minutes)
            departure_time += timedelta(minutes=delay_minutes)

        # Random initial platform assignment (some unassigned)
        platform = random.choice(platforms + [None, None])  # 30% chance of None

        # Train types
        train_types = ['EXPRESS', 'LOCAL', 'FREIGHT', 'PASSENGER']
        train_type = random.choice(train_types)

        # Capacity based on train type
        capacity_map = {
            'EXPRESS': random.randint(300, 500),
            'LOCAL': random.randint(200, 400),
            'FREIGHT': 0,  # No passenger capacity
            'PASSENGER': random.randint(150, 300)
        }
        capacity = capacity_map[train_type]

        train_data = {
            'train_id': train_id,
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'platform': platform,
            'delay_minutes': delay_minutes,
            'capacity': capacity,
            'train_type': train_type,
            'status': 'SCHEDULED' if delay_minutes == 0 else 'DELAYED'
        }

        trains_data.append(train_data)

    # Create DataFrame
    df = pd.DataFrame(trains_data)

    # Sort by arrival time
    df = df.sort_values('arrival_time').reset_index(drop=True)

    return df


def generate_mock_platform_status(platforms=None):
    """
    Generate mock platform status data.

    Args:
        platforms: List of platform IDs

    Returns:
        pandas.DataFrame: Platform status data
    """
    if platforms is None:
        settings = load_settings()
        platforms = settings['simulation']['platforms']

    platform_data = []

    for platform_id in platforms:
        # Random availability (90% chance of being available)
        is_available = random.random() > 0.1

        # Random capacity (most platforms can handle 1 train, some can handle 2)
        capacity = random.choice([1, 1, 1, 2])

        platform_info = {
            'platform_id': platform_id,
            'is_available': is_available,
            'capacity': capacity,
            'current_occupancy': 0,
            'maintenance_scheduled': random.random() < 0.05,  # 5% chance
            'last_updated': datetime.now()
        }

        platform_data.append(platform_info)

    return pd.DataFrame(platform_data)


def generate_mock_historical_data(days=30, trains_per_day=50):
    """
    Generate mock historical data for ML training.

    Args:
        days: Number of days of historical data
        trains_per_day: Average trains per day

    Returns:
        pandas.DataFrame: Historical train performance data
    """
    historical_data = []

    for day in range(days):
        date = datetime.now() - timedelta(days=days - day)
        daily_trains = int(np.random.poisson(trains_per_day))

        for i in range(daily_trains):
            train_id = f"H{day:02d}T{i:03d}"

            # Schedule time
            scheduled_hour = random.randint(6, 22)
            scheduled_minute = random.randint(0, 59)
            scheduled_time = date.replace(
                hour=scheduled_hour,
                minute=scheduled_minute,
                second=0,
                microsecond=0
            )

            # Actual delay (correlated with time of day and day of week)
            hour_factor = 1.5 if 7 <= scheduled_hour <= 9 or 17 <= scheduled_hour <= 19 else 1.0
            weekend_factor = 0.7 if date.weekday() >= 5 else 1.0
            weather_factor = random.uniform(0.8, 1.3)

            base_delay = np.random.exponential(2) * hour_factor * weekend_factor * weather_factor
            delay_minutes = max(0, int(base_delay))

            historical_record = {
                'train_id': train_id,
                'date': date.date(),
                'scheduled_time': scheduled_time,
                'actual_arrival': scheduled_time + timedelta(minutes=delay_minutes),
                'delay_minutes': delay_minutes,
                'day_of_week': date.weekday(),
                'hour_of_day': scheduled_hour,
                'is_weekend': date.weekday() >= 5,
                'weather_factor': weather_factor
            }

            historical_data.append(historical_record)

    return pd.DataFrame(historical_data)


# Utility functions for testing
def get_mock_trains(num_trains=10):
    """Simple function to get mock train data (for testing)."""
    return generate_mock_trains(num_trains)


def get_mock_platforms():
    """Get mock platform data."""
    return generate_mock_platform_status()


if __name__ == "__main__":
    # Demo usage
    print("Generating mock railway data...")

    # Generate train data
    trains_df = generate_mock_trains(15)
    print(f"\nGenerated {len(trains_df)} trains:")
    print(trains_df[['train_id', 'arrival_time', 'departure_time', 'platform', 'delay_minutes']].head(10))

    # Generate platform data
    platforms_df = generate_mock_platform_status()
    print(f"\nGenerated {len(platforms_df)} platforms:")
    print(platforms_df)

    # Generate historical data
    historical_df = generate_mock_historical_data(days=7, trains_per_day=20)
    print(f"\nGenerated {len(historical_df)} historical records")
    print(f"Average delay: {historical_df['delay_minutes'].mean():.1f} minutes")

