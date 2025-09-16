# scripts/maintenance.py
"""
Maintenance utilities for railway optimization system.
"""

import os
import logging
import sqlite3
from datetime import datetime, timedelta


def cleanup_old_logs(log_dir="logs", days_to_keep=30):
    """Remove log files older than specified days."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if not os.path.exists(log_dir):
        logger.info("Log directory does not exist")
        return

    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    removed_count = 0

    for filename in os.listdir(log_dir):
        filepath = os.path.join(log_dir, filename)

        if os.path.isfile(filepath):
            file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))

            if file_modified < cutoff_date:
                os.remove(filepath)
                removed_count += 1
                logger.info(f"Removed old log file: {filename}")

    logger.info(f"Cleanup complete. Removed {removed_count} old log files.")


def archive_optimization_results(db_path="railway.db", days_to_keep=90):
    """Archive old optimization results."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        # Count records to archive
        cursor.execute(
            "SELECT COUNT(*) FROM optimization_results WHERE run_timestamp < ?",
            (cutoff_date,)
        )
        count = cursor.fetchone()[0]

        if count > 0:
            # In a real system, you might move to archive table instead of delete
            cursor.execute(
                "DELETE FROM optimization_results WHERE run_timestamp < ?",
                (cutoff_date,)
            )

            conn.commit()
            logger.info(f"Archived {count} old optimization results")
        else:
            logger.info("No old optimization results to archive")

    except Exception as e:
        logger.error(f"Archive operation failed: {e}")
    finally:
        if conn:
            conn.close()


def system_health_check():
    """Perform basic system health checks."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    checks = {
        'database_accessible': False,
        'config_files_exist': False,
        'log_directory_writable': False
    }

    # Check database
    try:
        conn = sqlite3.connect("railway.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        checks['database_accessible'] = True
        conn.close()
    except Exception as e:
        logger.error(f"Database check failed: {e}")

    # Check config files
    config_files = ['config/settings.yaml']
    checks['config_files_exist'] = all(os.path.exists(f) for f in config_files)

    # Check log directory
    try:
        os.makedirs("logs", exist_ok=True)
        test_file = "logs/health_check.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        checks['log_directory_writable'] = True
    except Exception as e:
        logger.error(f"Log directory check failed: {e}")

    # Report results
    logger.info("System health check results:")
    for check, status in checks.items():
        status_str = "PASS" if status else "FAIL"
        logger.info(f"  {check}: {status_str}")

    return all(checks.values())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "cleanup":
            cleanup_old_logs()
        elif command == "archive":
            archive_optimization_results()
        elif command == "health":
            system_health_check()
        else:
            print("Usage: python maintenance.py [cleanup|archive|health]")
    else:
        print("Running all maintenance tasks...")
        cleanup_old_logs()
        archive_optimization_results()
        system_health_check()

