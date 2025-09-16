"""
Enhanced railway optimization dashboard widget with comprehensive report generation.
Saves reports to: railway-optimization-project/reports/
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTableWidget, QTableWidgetItem, QLabel, QTextEdit,
                           QHeaderView, QMessageBox, QApplication, QProgressBar,
                           QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta
import logging
import random
import json

class DashboardWidget(QWidget):
    """Enhanced dashboard widget with comprehensive report generation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.current_trains_df = None
        self.optimization_history = []  # Store optimization results
        self.auto_refresh_enabled = True

        # Create reports directory in the specific project path
        # Get the current working directory (should be railway-optimization-project)
        project_dir = os.getcwd()
        self.reports_dir = os.path.join(project_dir, 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

        # Log the reports directory for confirmation
        self.logger.info(f"Reports directory: {self.reports_dir}")

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

        subtitle = QLabel("Real-time Train Schedule Management & Platform Optimization with Report Generation")
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

        self.save_report_btn = QPushButton("📄 Save Report")
        self.save_report_btn.clicked.connect(self.save_optimization_report)
        self.save_report_btn.setToolTip("Save detailed optimization report")
        self.save_report_btn.setEnabled(False)  # Enable after optimization
        controls_layout.addWidget(self.save_report_btn)

        self.export_data_btn = QPushButton("📊 Export Data")
        self.export_data_btn.clicked.connect(self.export_train_data)
        self.export_data_btn.setToolTip("Export current train data to CSV")
        controls_layout.addWidget(self.export_data_btn)

        self.auto_refresh_btn = QPushButton("🔄 Auto Refresh: ON")
        self.auto_refresh_btn.clicked.connect(self.toggle_auto_refresh)
        self.auto_refresh_btn.setToolTip("Toggle automatic data refresh")
        controls_layout.addWidget(self.auto_refresh_btn)

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
        self.status_text.setPlainText(f"🚀 Railway Optimization System Ready\n📡 Waiting for user commands...\n💡 Tip: Run optimization then click 'Save Report' to generate detailed analysis!\n📁 Reports will be saved to: {self.reports_dir}")
        layout.addWidget(self.status_text)

        self.setLayout(layout)

        # Load initial data
        self.refresh_data()

    def setup_trains_table(self):
        """Setup the trains data table."""
        self.trains_table = QTableWidget()
        self.trains_table.setColumnCount(8)
        self.trains_table.setHorizontalHeaderLabels([
            "Train ID", "Arrival Time", "Departure Time",
            "Original Platform", "Optimized Platform", "Delay (min)", "Status", "Priority"
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
        self.auto_refresh_timer.start(15000)  # Refresh every 15 seconds

    def toggle_auto_refresh(self):
        """Toggle automatic refresh on/off."""
        if self.auto_refresh_enabled:
            self.auto_refresh_timer.stop()
            self.auto_refresh_btn.setText("🔄 Auto Refresh: OFF")
            self.auto_refresh_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
            self.auto_refresh_enabled = False
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ⏸️  Auto-refresh disabled")
        else:
            self.auto_refresh_timer.start(15000)
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

            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Data refreshed - {len(self.current_trains_df)} trains loaded")

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
            train_id = f"T{i+1:03d}"

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
                [0, 0, 0, 0, 0, 1, 2, 3, 5, 8, 10, 15, 20, 25],
                weights=[40, 20, 15, 10, 8, 4, 2, 1, 1, 1, 1, 1, 1, 1]
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

            # Priority based on train type and delay
            train_type = random.choice(train_types)
            if train_type == 'EXPRESS':
                priority = 'HIGH'
            elif train_type == 'PASSENGER':
                priority = 'MEDIUM'
            else:
                priority = 'LOW'

            # If major delay, increase priority
            if delay > 15:
                priority = 'URGENT'

            # Random platform assignment (some unassigned)
            platform = random.choice(platforms + [None, None])  # 30% chance unassigned

            train_data = {
                'train_id': train_id,
                'arrival_time': arrival_time,
                'departure_time': departure_time,
                'original_platform': platform,
                'platform': platform,  # Keep for compatibility
                'delay_minutes': delay,
                'train_type': train_type,
                'status': status,
                'priority': priority,
                'optimized_platform': '',
                'optimization_reason': ''  # Why this assignment was made
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

            # Original Platform
            original_platform = train.get('original_platform', 'Unassigned')
            if pd.isnull(original_platform):
                original_platform = 'Unassigned'
            self.trains_table.setItem(i, 3, QTableWidgetItem(str(original_platform)))

            # Optimized Platform
            optimized_platform = train.get('optimized_platform', '')
            self.trains_table.setItem(i, 4, QTableWidgetItem(str(optimized_platform)))

            # Delay
            delay = train.get('delay_minutes', 0)
            self.trains_table.setItem(i, 5, QTableWidgetItem(str(delay)))

            # Status
            status = train.get('status', 'UNKNOWN')
            self.trains_table.setItem(i, 6, QTableWidgetItem(status))

            # Priority
            priority = train.get('priority', 'MEDIUM')
            self.trains_table.setItem(i, 7, QTableWidgetItem(priority))

    def run_optimization(self):
        """Run the optimization algorithm with detailed reasoning."""
        if self.current_trains_df is None or self.current_trains_df.empty:
            QMessageBox.warning(self, "Warning", "No train data available. Please refresh data first.")
            return

        try:
            self.status_label.setText("● Optimizing...")
            self.status_label.setStyleSheet("color: #FF9800; font-weight: bold;")

            start_time = datetime.now()

            self.status_text.append(f"[{start_time.strftime('%H:%M:%S')}] ⚡ Starting advanced platform optimization...")
            self.status_text.append(f"[{start_time.strftime('%H:%M:%S')}] 📋 Processing {len(self.current_trains_df)} trains...")

            # Advanced assignment algorithm with reasoning
            platforms = ['P1', 'P2', 'P3', 'P4', 'P5']
            assignments = {}
            assignment_reasons = {}
            platform_schedule = {p: [] for p in platforms}
            conflicts_resolved = 0
            priority_changes = 0

            # Sort trains by priority and arrival time
            priority_order = {'URGENT': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
            sorted_trains = self.current_trains_df.copy()
            sorted_trains['priority_score'] = sorted_trains['priority'].map(priority_order)
            sorted_trains = sorted_trains.sort_values(['priority_score', 'arrival_time'], ascending=[False, True])

            for _, train in sorted_trains.iterrows():
                train_id = train['train_id']
                arrival = train['arrival_time']
                departure = train['departure_time']
                priority = train['priority']
                original_platform = train['original_platform']

                # Find best platform with detailed reasoning
                best_platform = None
                min_conflicts = float('inf')
                reason = ""

                # Check if original platform is available and good
                if pd.notnull(original_platform) and original_platform in platforms:
                    conflicts = self.count_conflicts(original_platform, arrival, departure, platform_schedule)
                    if conflicts == 0:
                        best_platform = original_platform
                        reason = f"Kept original assignment {original_platform} (no conflicts)"
                    else:
                        reason = f"Original platform {original_platform} had {conflicts} conflicts, reassigning"

                # If original platform not suitable, find best alternative
                if best_platform is None:
                    for platform in platforms:
                        conflicts = self.count_conflicts(platform, arrival, departure, platform_schedule)

                        if conflicts < min_conflicts:
                            min_conflicts = conflicts
                            best_platform = platform

                    if min_conflicts > 0:
                        conflicts_resolved += min_conflicts
                        reason += f" -> Assigned to {best_platform} (minimized conflicts: {min_conflicts})"
                    else:
                        reason += f" -> Assigned to {best_platform} (conflict-free)"

                    if priority in ['URGENT', 'HIGH']:
                        priority_changes += 1
                        reason += f" [Priority {priority} train]"

                # Assign to best platform
                if best_platform:
                    assignments[train_id] = best_platform
                    assignment_reasons[train_id] = reason
                    platform_schedule[best_platform].append((arrival, departure, train_id))
                else:
                    # Emergency fallback
                    fallback_platform = platforms[len(assignments) % len(platforms)]
                    assignments[train_id] = fallback_platform
                    assignment_reasons[train_id] = f"Emergency assignment to {fallback_platform} (all platforms busy)"
                    platform_schedule[fallback_platform].append((arrival, departure, train_id))

            # Update results with reasoning
            self.update_optimized_assignments(assignments, assignment_reasons)

            # Calculate comprehensive statistics
            end_time = datetime.now()
            solve_time = (end_time - start_time).total_seconds()

            unassigned_before = len(self.current_trains_df[self.current_trains_df['original_platform'].isnull()])
            total_delay = self.current_trains_df['delay_minutes'].sum()
            avg_delay = self.current_trains_df['delay_minutes'].mean()

            # Platform utilization analysis
            platform_counts = {}
            for platform in platforms:
                platform_counts[platform] = sum(1 for p in assignments.values() if p == platform)

            # Priority distribution
            priority_stats = self.current_trains_df['priority'].value_counts().to_dict()

            # Store optimization result for report
            optimization_result = {
                'timestamp': start_time,
                'solve_time_seconds': solve_time,
                'total_trains': len(self.current_trains_df),
                'assignments': assignments,
                'assignment_reasons': assignment_reasons,
                'unassigned_before': unassigned_before,
                'total_delay': total_delay,
                'avg_delay': avg_delay,
                'conflicts_resolved': conflicts_resolved,
                'priority_changes': priority_changes,
                'platform_utilization': platform_counts,
                'priority_distribution': priority_stats,
                'trains_data': self.current_trains_df.copy()
            }

            self.optimization_history.append(optimization_result)

            # Display results
            self.status_text.append(f"[{end_time.strftime('%H:%M:%S')}] ✅ Advanced optimization completed!")
            self.status_text.append(f"[{end_time.strftime('%H:%M:%S')}] 📊 Results Summary:")
            self.status_text.append(f"    • Solve time: {solve_time:.2f} seconds")
            self.status_text.append(f"    • Trains assigned: {len(assignments)}")
            self.status_text.append(f"    • Conflicts resolved: {conflicts_resolved}")
            self.status_text.append(f"    • Priority assignments: {priority_changes}")
            self.status_text.append(f"    • Previously unassigned: {unassigned_before}")
            self.status_text.append(f"    • Total delay: {total_delay} minutes")
            self.status_text.append(f"    • Average delay: {avg_delay:.1f} minutes")
            self.status_text.append(f"[{end_time.strftime('%H:%M:%S')}] 🏁 Platform utilization:")
            for platform, count in platform_counts.items():
                utilization = (count / len(assignments)) * 100
                self.status_text.append(f"    • {platform}: {count} trains ({utilization:.1f}%)")

            self.status_label.setText("● Optimized")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

            # Enable report saving
            self.save_report_btn.setEnabled(True)
            self.status_text.append(f"[{end_time.strftime('%H:%M:%S')}] 📄 Report ready - Click 'Save Report' to generate detailed analysis")

        except Exception as e:
            self.logger.error(f"Optimization failed: {e}")
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Optimization failed: {e}")
            self.status_label.setText("● Error")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")

    def count_conflicts(self, platform, arrival, departure, platform_schedule):
        """Count time conflicts for a platform."""
        conflicts = 0
        buffer = timedelta(minutes=5)

        for scheduled_arrival, scheduled_departure, _ in platform_schedule[platform]:
            if not (departure + buffer <= scheduled_arrival or
                   scheduled_departure + buffer <= arrival):
                conflicts += 1

        return conflicts

    def update_optimized_assignments(self, assignments, reasons):
        """Update table with optimized platform assignments and reasons."""
        # Update the dataframe
        for train_id, platform in assignments.items():
            mask = self.current_trains_df['train_id'] == train_id
            self.current_trains_df.loc[mask, 'optimized_platform'] = platform
            if train_id in reasons:
                self.current_trains_df.loc[mask, 'optimization_reason'] = reasons[train_id]

        # Update the table display
        for i in range(self.trains_table.rowCount()):
            train_id_item = self.trains_table.item(i, 0)
            if train_id_item:
                train_id = train_id_item.text()
                if train_id in assignments:
                    optimized_platform = assignments[train_id]
                    opt_item = QTableWidgetItem(optimized_platform)
                    self.trains_table.setItem(i, 4, opt_item)

    def save_optimization_report(self):
        """Save detailed optimization report."""
        if not self.optimization_history:
            QMessageBox.warning(self, "No Data", "No optimization results to save. Please run optimization first.")
            return

        try:
            # Get latest optimization result
            latest_result = self.optimization_history[-1]
            timestamp = latest_result['timestamp']

            # Generate filename
            filename = f"optimization_report_{timestamp.strftime('%Y%m%d_%H%M%S')}"

            # Let user choose format and location (default to project reports directory)
            default_path = os.path.join(self.reports_dir, filename)
            file_path, selected_filter = QFileDialog.getSaveFileName(
                self,
                "Save Optimization Report",
                default_path,
                "Text Report (*.txt);;CSV Data (*.csv);;JSON Data (*.json)"
            )

            if not file_path:
                return  # User cancelled

            if selected_filter == "Text Report (*.txt)":
                self.save_text_report(file_path, latest_result)
            elif selected_filter == "CSV Data (*.csv)":
                self.save_csv_report(file_path, latest_result)
            else:  # JSON
                self.save_json_report(file_path, latest_result)

            QMessageBox.information(self, "Report Saved", f"Optimization report saved successfully to:\n{file_path}\n\nReports directory: {self.reports_dir}")
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📄 Report saved: {os.path.basename(file_path)}")
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📁 Full path: {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save report:\n{str(e)}")
            self.logger.error(f"Failed to save report: {e}")

    def save_text_report(self, file_path, result):
        """Save detailed text report."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAILWAY OPTIMIZATION DETAILED REPORT\n")
            f.write("=" * 80 + "\n\n")

            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Optimization Date/Time: {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Trains Processed: {result['total_trains']}\n")
            f.write(f"Optimization Time: {result['solve_time_seconds']:.2f} seconds\n")
            f.write(f"Conflicts Resolved: {result['conflicts_resolved']}\n")
            f.write(f"Priority Reassignments: {result['priority_changes']}\n")
            f.write(f"Average Delay: {result['avg_delay']:.1f} minutes\n\n")

            # Platform Utilization Analysis
            f.write("PLATFORM UTILIZATION ANALYSIS\n")
            f.write("-" * 40 + "\n")
            total_assignments = sum(result['platform_utilization'].values())
            for platform, count in result['platform_utilization'].items():
                utilization = (count / total_assignments) * 100 if total_assignments > 0 else 0
                f.write(f"{platform}: {count} trains ({utilization:.1f}% utilization)\n")
            f.write("\n")

            # Priority Distribution
            f.write("TRAIN PRIORITY DISTRIBUTION\n")
            f.write("-" * 40 + "\n")
            for priority, count in result['priority_distribution'].items():
                percentage = (count / result['total_trains']) * 100
                f.write(f"{priority}: {count} trains ({percentage:.1f}%)\n")
            f.write("\n")

            # Detailed Assignment Reasoning
            f.write("DETAILED ASSIGNMENT DECISIONS\n")
            f.write("-" * 40 + "\n")
            for train_id, reason in result['assignment_reasons'].items():
                platform = result['assignments'][train_id]
                f.write(f"{train_id} -> {platform}: {reason}\n")
            f.write("\n")

            # Train Details Table
            f.write("COMPLETE TRAIN SCHEDULE\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'Train ID':<8} {'Arrival':<8} {'Departure':<10} {'Original':<10} {'Optimized':<10} {'Delay':<6} {'Priority':<8} {'Status'}\n")
            f.write("-" * 80 + "\n")

            trains_df = result['trains_data']
            for _, train in trains_df.iterrows():
                arrival = train['arrival_time'].strftime('%H:%M')
                departure = train['departure_time'].strftime('%H:%M')
                original = str(train['original_platform']) if pd.notnull(train['original_platform']) else 'None'
                optimized = train['optimized_platform']

                f.write(f"{train['train_id']:<8} {arrival:<8} {departure:<10} {original:<10} {optimized:<10} "
                       f"{train['delay_minutes']:<6} {train['priority']:<8} {train['status']}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("Report generated by Railway Optimization System\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def save_csv_report(self, file_path, result):
        """Save optimization data as CSV."""
        trains_df = result['trains_data'].copy()

        # Add optimization results to dataframe
        for train_id, platform in result['assignments'].items():
            mask = trains_df['train_id'] == train_id
            trains_df.loc[mask, 'optimized_platform'] = platform
            if train_id in result['assignment_reasons']:
                trains_df.loc[mask, 'optimization_reason'] = result['assignment_reasons'][train_id]

        # Add metadata
        trains_df['optimization_timestamp'] = result['timestamp']
        trains_df['solve_time_seconds'] = result['solve_time_seconds']

        trains_df.to_csv(file_path, index=False)

    def save_json_report(self, file_path, result):
        """Save complete optimization data as JSON."""
        # Convert datetime objects to strings for JSON serialization
        json_result = result.copy()
        json_result['timestamp'] = result['timestamp'].isoformat()

        # Convert dataframe to dict
        trains_df = result['trains_data'].copy()
        trains_df['arrival_time'] = trains_df['arrival_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        trains_df['departure_time'] = trains_df['departure_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        json_result['trains_data'] = trains_df.to_dict('records')

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, indent=2, ensure_ascii=False)

    def export_train_data(self):
        """Export current train data to CSV."""
        if self.current_trains_df is None or self.current_trains_df.empty:
            QMessageBox.warning(self, "No Data", "No train data to export.")
            return

        try:
            filename = f"train_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            default_path = os.path.join(self.reports_dir, filename)
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Train Data",
                default_path,
                "CSV Files (*.csv)"
            )

            if file_path:
                self.current_trains_df.to_csv(file_path, index=False)
                QMessageBox.information(self, "Export Successful", f"Train data exported to:\n{file_path}\n\nReports directory: {self.reports_dir}")
                self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Data exported: {os.path.basename(file_path)}")
                self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📁 Full path: {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export data:\n{str(e)}")

    def clear_optimization_results(self):
        """Clear optimization results."""
        try:
            if self.current_trains_df is not None:
                self.current_trains_df['optimized_platform'] = ''
                self.update_trains_table()
                self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🗑️  Optimization results cleared")
        except Exception as e:
            self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error clearing results: {e}")

# Test the enhanced dashboard
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DashboardWidget()
    widget.show()
    sys.exit(app.exec_())
