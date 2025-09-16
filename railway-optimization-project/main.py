# =============================================================================
# main.py - Entry point
# =============================================================================
"""
Main entry point for Railway Optimization Prototype.
"""

import sys
import os
import logging
from datetime import datetime


def setup_project_structure():
    """Create necessary directories and files."""
    directories = [
        'logs',
        'models',
        'exports',
        'config',
        'dashboards',
        'core',
        'core/optimization'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create settings.yaml if it doesn't exist
    settings_path = 'config/settings.yaml'
    if not os.path.exists(settings_path):
        default_settings = """# Railway Optimization Settings

solver:
  time_limit_ms: 5000
  enable_logging: true

simulation:
  num_trains: 15
  station_code: "NDLS"
  platforms: ["P1", "P2", "P3", "P4", "P5"]
  time_window_hours: 8

ui:
  refresh_interval_ms: 5000
  theme: "default"
"""
        with open(settings_path, 'w') as f:
            f.write(default_settings)


def main():
    """Main application entry point."""
    print("Railway Optimization Prototype")
    print("=" * 40)

    # Setup project structure
    setup_project_structure()

    # Setup logging
    log_filename = f"logs/railway_optimization_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting Railway Optimization Prototype")

    try:
        # Check if running in GUI mode
        if len(sys.argv) > 1 and sys.argv[1] == '--cli':
            # Command line mode
            print("Running in CLI mode...")
            import optimization
            result = optimization.run_optimization()
            optimization.print_optimization_results(result)
        else:
            # GUI mode (default)
            print("Starting GUI application...")
            from main_window import main as gui_main
            gui_main()

    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("\nPlease install required packages:")
        print("pip install PyQt5 pyyaml pandas numpy")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()