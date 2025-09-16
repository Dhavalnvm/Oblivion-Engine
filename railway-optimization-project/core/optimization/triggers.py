# core/optimization/triggers.py
"""
Optimization trigger logic.
"""

import time
import threading
from datetime import datetime, timedelta
import logging


class OptimizationTrigger:
    """Manages when to trigger optimization runs."""

    def __init__(self, solver, interval_minutes=5):
        self.solver = solver
        self.interval_minutes = interval_minutes
        self.is_running = False
        self.last_run = None
        self.logger = logging.getLogger(__name__)

    def start_scheduler(self):
        """Start automatic optimization scheduling."""
        self.is_running = True
        threading.Thread(target=self._run_scheduler, daemon=True).start()
        self.logger.info("Optimization scheduler started")

    def stop_scheduler(self):
        """Stop automatic scheduling."""
        self.is_running = False
        self.logger.info("Optimization scheduler stopped")

    def _run_scheduler(self):
        """Run scheduled optimization."""
        while self.is_running:
            try:
                if self._should_run_optimization():
                    self._trigger_optimization()
                    self.last_run = datetime.now()

                time.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}")

    def _should_run_optimization(self):
        """Determine if optimization should run."""
        if self.last_run is None:
            return True

        time_since_last = datetime.now() - self.last_run
        return time_since_last >= timedelta(minutes=self.interval_minutes)

    def _trigger_optimization(self):
        """Trigger optimization run."""
        self.logger.info("Triggering scheduled optimization")
        # In full system: would trigger solver with current data


