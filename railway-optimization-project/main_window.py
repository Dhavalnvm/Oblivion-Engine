# =============================================================================
# main_window.py - Main PyQt Window
# =============================================================================
"""
Main PyQt application window for railway optimization.
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                           QWidget, QVBoxLayout, QLabel, QMenuBar, 
                           QStatusBar, QAction, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import logging
from datetime import datetime

# Import dashboard components
from dashboards.dashboard import DashboardWidget

class OptimizationTab(QWidget):
    """Optimization configuration and control tab."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize optimization tab UI."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Optimization Configuration")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Info panel
        info_label = QLabel("""
        Optimization Configuration Panel
        
        Current features:
        • Simple platform assignment algorithm
        • Mock train data generation
        • Real-time dashboard updates
        
        Future features:
        • CP-SAT constraint solver integration
        • Advanced scheduling optimization
        • Machine learning predictions
        • Multi-objective optimization
        """)
        info_label.setAlignment(Qt.AlignTop)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        self.setLayout(layout)

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.init_ui()
        self.setup_logging()
    
    def init_ui(self):
        """Initialize the main window UI."""
        self.setWindowTitle("Railway Optimization Prototype v1.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs
        self.dashboard_tab = DashboardWidget()
        self.optimization_tab = OptimizationTab()
        
        # Add tabs to tab widget
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.optimization_tab, "⚙️ Configuration")
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Railway Optimization System Ready")
        
        # Style the application
        self.apply_stylesheet()
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Export action
        export_action = QAction('Export Data', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # Refresh action
        refresh_action = QAction('Refresh Data', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def apply_stylesheet(self):
        """Apply custom stylesheet to the application."""
        stylesheet = """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
                border-radius: 5px;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #2196F3;
            }
            
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #eee;
                background-color: white;
                border-radius: 5px;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            
            QTableWidget::item:selected {
                background-color: #e3f2fd;
            }
            
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
            
            QTextEdit {
                border: 1px solid #ddd;
                background-color: #fafafa;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                border-radius: 5px;
                padding: 5px;
            }
            
            QLabel {
                color: #333;
            }
        """
        self.setStyleSheet(stylesheet)
    
    def setup_logging(self):
        """Setup application logging."""
        self.logger.info("Railway Optimization Application Started")
    
    def export_data(self):
        """Export current data to file."""
        try:
            if hasattr(self.dashboard_tab, 'current_trains_df') and self.dashboard_tab.current_trains_df is not None:
                filename = f"train_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                self.dashboard_tab.current_trains_df.to_csv(filename, index=False)
                QMessageBox.information(self, "Export Successful", f"Data exported to {filename}")
                self.status_bar.showMessage(f"Data exported to {filename}")
            else:
                QMessageBox.warning(self, "Export Failed", "No data available to export")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export data:\n{str(e)}")
    
    def refresh_all(self):
        """Refresh all application data."""
        try:
            self.dashboard_tab.refresh_data()
            self.status_bar.showMessage("All data refreshed")
        except Exception as e:
            QMessageBox.critical(self, "Refresh Error", f"Failed to refresh data:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
        <h3>Railway Optimization Prototype</h3>
        <p>A PyQt-based railway optimization system demonstrating:</p>
        <ul>
        <li>✅ Mock train data generation</li>
        <li>✅ Simple platform assignment</li>
        <li>✅ Real-time dashboard visualization</li>
        <li>✅ Data export capabilities</li>
        </ul>
        
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Technologies:</b> PyQt5, Python, Pandas</p>
        
        <p><b>Status:</b> This is a working prototype. Advanced features like 
        CP-SAT optimization and machine learning can be added incrementally.</p>
        """
        
        QMessageBox.about(self, "About Railway Optimization", about_text)
    
    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(
            self, 'Exit Confirmation',
            'Are you sure you want to exit the Railway Optimization System?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.logger.info("Application closing")
            event.accept()
        else:
            event.ignore()

def main():
    """Main application entry point."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Railway Optimization Prototype")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
