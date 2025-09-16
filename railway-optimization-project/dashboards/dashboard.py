"""
Railway optimization dashboard widget.
"""

import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QTextEdit,
                             QHeaderView, QMessageBox, QApplication, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta
import logging
import random


class DashboardWidget(QWidget):
    """Main dashboard widget for railway optimization."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.current_trains_df = None
        self.auto_refresh_enabled = True

        self.init_ui()
        self.setup_auto_refresh()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()

        # Title section
        title_layout = QVBoxLayout()
        title = QLabel("🚂 Railway Optimization Dashboard")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2196F3; margin: 10px;")
        title_layout.addWidget(title)

        subtitle = QLabel("Real-time Train Schedule Management & Platform Optimization")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 15px;")
        title_layout.addWidget(subtitle)

        layout.addLayout(title_layout)

        # Control buttons
        controls_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("🔄 Refresh Data")
        self.refresh_btn.clicked.connect(self.refresh_data)
        self.refresh_btn.setToolTip("Refresh train data with new mock information")
        controls_layout.addWidget(self.refresh_btn)

        self.optimize_btn = QPushButton("⚡ Run Optimization")
        self.optimize_btn.clicked.connect(self.run_optimization)
        self.optimize_btn.setToolTip("Optimize platform assignments for all trains")
        controls_layout.addWidget(self.optimize_btn)

        self.auto_refresh_btn = QPushButton("🔄 Auto Refresh: ON")
        self.auto_refresh_btn.clicked.connect(self.toggle_auto_refresh)
        self.auto_refresh_btn.setToolTip("Toggle automatic data refresh")
        controls_layout.addWidget(self.auto_refresh_btn)

        self.clear_btn = QPushButton("🗑️ Clear Results")
        self.clear_btn.clicked.connect(self.clear_optimization_results)
        self.clear_btn.setToolTip("Clear optimization results")
        controls_layout.addWidget(self.clear_btn)

        controls_layout.addStretch()

        # Status indicators
        self.status_label = QLabel("● System Ready")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        controls_layout.addWidget(self.status_label)

        layout.addLayout(controls_layout)

        # Train data table
        table_label = QLabel("📋 Current Train Schedule:")
        table_label.setFont(QFont("Arial", 12, QFont.Bold))
        table_label.setStyleSheet("margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(table_label)

        self.setup_trains_table()
        layout.addWidget(self.trains_table)

        # Status and results section
        status_label = QLabel("📊 System Log & Optimization Results:")
        status_label.setFont(QFont("Arial", 12, QFont.Bold))
        status_label.setStyleSheet("margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(status_label)

        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setPlainText("🚀 Railway Optimization System Ready\n📡 Waiting for user commands...")
        layout.addWidget(self.status_text)

        self.setLayout(layout)

        # Load initial data
        self.refresh_data()

    def setup_trains_table(self):
        """Setup the trains data table."""
        self.trains_table = QTableWidget()
        self.trains_table.setColumnCount(7)
        self.trains_table.setHorizontalHeaderLabels([
            "Train ID", "Arrival Time", "Departure Time",
            "Current Platform", "Optimized Platform", "Delay (min)", "Status"
        ])

        # Make table fill available space
        header = self.trains_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Make table read-only
        self.trains_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Set alternating row colors
        self.trains_table.setAlternatingRowColors(True)

    def setup_auto_refresh(self):
        """Setup automatic data refresh timer."""
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.refresh_data)
        self.auto_refresh_timer.start(10000)  # Refresh every 10 seconds

    def toggle_auto_refresh(self):
        """Toggle automatic refresh on/off."""
        if self.auto_refresh_enabled:
            self.auto_refresh_timer.stop()
            self.auto_refresh_btn.setText("🔄 Auto Refresh: OFF")
            self.auto_refresh_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
            self.auto_refresh_enabled = False
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ⏸️  Auto-refresh disabled")
        else:
            self.auto_refresh_timer.start(10000)
            self.auto_refresh_btn.setText("🔄 Auto Refresh: ON")
            self.auto_refresh_btn.setStyleSheet("")  # Reset to default
            self.auto_refresh_enabled = True
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ▶️  Auto-refresh enabled")

    def refresh_data(self):
        """Refresh train data."""
        try:
            self.status_label.setText("● Refreshing...")
            self.status_label.setStyleSheet("color: #FF9800; font-weight: bold;")

            # Generate fresh mock data
            self.current_trains_df = self.generate_mock_data()
            self.update_trains_table()

            self.status_text.append(
                f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Data refreshed - {len(self.current_trains_df)} trains loaded")

            self.status_label.setText("● System Ready")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        except Exception as e:
            self.logger.error(f"Failed to refresh data: {e}")
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error refreshing data: {e}")
            self.status_label.setText("● Error")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")

    def generate_mock_data(self):
        """Generate realistic mock train data."""
        base_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
        platforms = ['P1', 'P2', 'P3', 'P4', 'P5']
        train_types = ['EXPRESS', 'LOCAL', 'FREIGHT', 'PASSENGER']

        trains_data = []
        for i in range(12):
            train_id = f"T{i + 1:03d}"

            # Random arrival time within 8 hours
            arrival_offset = timedelta(
                hours=random.uniform(0, 8),
                minutes=random.randint(0, 59)
            )
            arrival_time = base_time + arrival_offset

            # Departure 15-45 minutes after arrival
            departure_time = arrival_time + timedelta(minutes=random.randint(15, 45))

            # Delay with realistic distribution
            delay = random.choices(
                [0, 0, 0, 0, 0, 1, 2, 3, 5, 8, 10, 15, 20, 25],  # Realistic delay distribution
                weights=[40, 20, 15, 10, 8, 4, 2, 1, 1, 1, 1, 1, 1, 1]  # Most trains on time
            )[0]

            # Adjust times for delay
            if delay > 0:
                arrival_time += timedelta(minutes=delay)
                departure_time += timedelta(minutes=delay)

            # Status based on delay
            if delay == 0:
                status = "ON TIME"
            elif delay <= 5:
                status = "MINOR DELAY"
            elif delay <= 15:
                status = "DELAYED"
            else:
                status = "MAJOR DELAY"

            # Random platform assignment (some unassigned)
            platform = random.choice(platforms + [None, None])  # 30% chance unassigned

            train_data = {
                'train_id': train_id,
                'arrival_time': arrival_time,
                'departure_time': departure_time,
                'platform': platform,
                'delay_minutes': delay,
                'train_type': random.choice(train_types),
                'status': status,
                'optimized_platform': ''
            }

            trains_data.append(train_data)

        df = pd.DataFrame(trains_data)
        return df.sort_values('arrival_time').reset_index(drop=True)

    def update_trains_table(self):
        """Update the trains table with current data."""
        if self.current_trains_df is None or self.current_trains_df.empty:
            return

        df = self.current_trains_df
        self.trains_table.setRowCount(len(df))

        for i, (_, train) in enumerate(df.iterrows()):
            # Train ID
            train_id_item = QTableWidgetItem(str(train['train_id']))
            train_id_item.setFont(QFont("Arial", 10, QFont.Bold))
            self.trains_table.setItem(i, 0, train_id_item)

            # Arrival Time
            arrival_str = train['arrival_time'].strftime('%H:%M') if pd.notnull(train['arrival_time']) else "N/A"
            self.trains_table.setItem(i, 1, QTableWidgetItem(arrival_str))

            # Departure Time
            departure_str = train['departure_time'].strftime('%H:%M') if pd.notnull(train['departure_time']) else "N/A"
            self.trains_table.setItem(i, 2, QTableWidgetItem(departure_str))

            # Current Platform
            current_platform = train.get('platform', 'Unassigned')
            if pd.isnull(current_platform):
                current_platform = 'Unassigned'
            platform_item = QTableWidgetItem(str(current_platform))
            self.trains_table.setItem(i, 3, platform_item)

            # Optimized Platform
            optimized_platform = train.get('optimized_platform', '')
            opt_item = QTableWidgetItem(str(optimized_platform))
            self.trains_table.setItem(i, 4, opt_item)

            # Delay
            delay = train.get('delay_minutes', 0)
            delay_item = QTableWidgetItem(str(delay))
            self.trains_table.setItem(i, 5, delay_item)

            # Status
            status = train.get('status', 'UNKNOWN')
            status_item = QTableWidgetItem(status)
            self.trains_table.setItem(i, 6, status_item)

    def run_optimization(self):
        """Run the optimization algorithm."""
        if self.current_trains_df is None or self.current_trains_df.empty:
            QMessageBox.warning(self, "Warning", "No train data available. Please refresh data first.")
            return

        try:
            self.status_label.setText("● Optimizing...")
            self.status_label.setStyleSheet("color: #FF9800; font-weight: bold;")

            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ⚡ Starting platform optimization...")
            self.status_text.append(
                f"[{datetime.now().strftime('%H:%M:%S')}] 📋 Processing {len(self.current_trains_df)} trains...")

            # Smart assignment algorithm
            platforms = ['P1', 'P2', 'P3', 'P4', 'P5']
            assignments = {}
            platform_schedule = {p: [] for p in platforms}

            # Sort trains by arrival time for better assignment
            sorted_trains = self.current_trains_df.sort_values('arrival_time')

            for _, train in sorted_trains.iterrows():
                train_id = train['train_id']
                arrival = train['arrival_time']
                departure = train['departure_time']

                # Find best platform (least conflicts)
                best_platform = None
                min_conflicts = float('inf')

                for platform in platforms:
                    conflicts = 0
                    for scheduled_arrival, scheduled_departure in platform_schedule[platform]:
                        # Check for time overlap with buffer
                        buffer = timedelta(minutes=5)
                        if not (departure + buffer <= scheduled_arrival or
                                scheduled_departure + buffer <= arrival):
                            conflicts += 1

                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_platform = platform

                # Assign to best platform
                if best_platform:
                    assignments[train_id] = best_platform
                    platform_schedule[best_platform].append((arrival, departure))
                else:
                    # Fallback to round-robin if all platforms busy
                    fallback_platform = platforms[len(assignments) % len(platforms)]
                    assignments[train_id] = fallback_platform
                    platform_schedule[fallback_platform].append((arrival, departure))

            # Update results
            self.update_optimized_assignments(assignments)

            # Calculate statistics
            unassigned_before = len(self.current_trains_df[self.current_trains_df['platform'].isnull()])
            total_delay = self.current_trains_df['delay_minutes'].sum()
            avg_delay = self.current_trains_df['delay_minutes'].mean()

            # Platform utilization
            platform_counts = {}
            for platform in platforms:
                platform_counts[platform] = sum(1 for p in assignments.values() if p == platform)

            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Optimization completed successfully!")
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Results:")
            self.status_text.append(f"    • Trains assigned: {len(assignments)}")
            self.status_text.append(f"    • Previously unassigned: {unassigned_before}")
            self.status_text.append(f"    • Total delay: {total_delay} minutes")
            self.status_text.append(f"    • Average delay: {avg_delay:.1f} minutes")
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🏁 Platform utilization:")
            for platform, count in platform_counts.items():
                self.status_text.append(f"    • {platform}: {count} trains")

            self.status_label.setText("● Optimized")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        except Exception as e:
            self.logger.error(f"Optimization failed: {e}")
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Optimization failed: {e}")
            self.status_label.setText("● Error")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")

    def update_optimized_assignments(self, assignments):
        """Update table with optimized platform assignments."""
        # Update the dataframe
        for train_id, platform in assignments.items():
            mask = self.current_trains_df['train_id'] == train_id
            self.current_trains_df.loc[mask, 'optimized_platform'] = platform

        # Update the table display
        for i in range(self.trains_table.rowCount()):
            train_id_item = self.trains_table.item(i, 0)
            if train_id_item:
                train_id = train_id_item.text()
                if train_id in assignments:
                    optimized_platform = assignments[train_id]
                    opt_item = QTableWidgetItem(optimized_platform)
                    self.trains_table.setItem(i, 4, opt_item)

    def clear_optimization_results(self):
        """Clear optimization results."""
        try:
            if self.current_trains_df is not None:
                self.current_trains_df['optimized_platform'] = ''
                self.update_trains_table()
                self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🗑️  Optimization results cleared")
        except Exception as e:
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error clearing results: {e}")


# Test the dashboard standalone
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DashboardWidget()
    widget.show()
    sys.exit(app.exec_())