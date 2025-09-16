# scripts/db_migration.py
"""
Database migration script.
"""

import sqlite3
import os
import logging


def create_database_schema(db_path="railway.db"):
    """Create database schema for railway optimization."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Trains table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trains (
                train_id TEXT PRIMARY KEY,
                arrival_time TIMESTAMP,
                departure_time TIMESTAMP,
                platform TEXT,
                delay_minutes INTEGER DEFAULT 0,
                capacity INTEGER DEFAULT 200,
                train_type TEXT DEFAULT 'EXPRESS',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Platforms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platforms (
                platform_id TEXT PRIMARY KEY,
                capacity INTEGER DEFAULT 1,
                is_available BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Optimization results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                solve_time_ms REAL,
                objective_value REAL,
                num_trains INTEGER,
                assignments TEXT  -- JSON string of platform assignments
            )
        ''')

        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_trains_time ON trains(arrival_time)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_timestamp ON optimization_results(run_timestamp)')

        conn.commit()
        logger.info(f"Database schema created successfully: {db_path}")

    except Exception as e:
        logger.error(f"Database migration failed: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_database_schema()

