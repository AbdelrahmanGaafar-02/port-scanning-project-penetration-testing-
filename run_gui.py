#!/usr/bin/env python3
"""
SecureScan GUI Launcher with Auto-Dependency Installation
"""
import sys
import subprocess
import os

def install_package(package):
    """Install a Python package using pip"""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    missing = []
    
    # Check for requests
    try:
        import requests
        print("✓ requests already installed")
    except ImportError:
        print("✗ requests not found")
        missing.append('requests')
    
    # Install missing packages
    if missing:
        print(f"\nInstalling missing dependencies: {', '.join(missing)}")
        for package in missing:
            if not install_package(package):
                print(f"\nWarning: Could not install {package}")
                print("The scanner will use fallback methods where possible.")
        
        # Verify installation
        try:
            import requests
            print("\n✓ All dependencies installed successfully!")
        except ImportError:
            print("\n⚠ Some dependencies could not be installed.")
            print("The scanner will run with limited functionality.")
            return False
    
    return True

def check_tkinter():
    """Check if tkinter is available (should be with Python)"""
    try:
        import tkinter
        print("✓ tkinter available")
        return True
    except ImportError:
        print("✗ tkinter not found")
        print("\nOn Ubuntu/Debian: sudo apt-get install python3-tk")
        print("On Fedora: sudo dnf install python3-tkinter")
        print("On Windows: Reinstall Python and ensure 'tcl/tk' is checked")
        return False

def main():
    """Launch the GUI application"""
    print("=" * 50)
    print("SecureScan GUI Launcher v2.0")
    print("=" * 50)
    print()
    
    # Check Python version
    print(f"Python version: {sys.version.split()[0]}")
    print()
    
    # Check tkinter first
    if not check_tkinter():
        print("\nCannot continue without tkinter.")
        sys.exit(1)
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("\nContinuing with limited functionality...")
    
    print("\n" + "=" * 50)
    print("FOR EDUCATIONAL PURPOSES ONLY")
    print("=" * 50)
    print()
    
    # Import and run GUI
    try:
        from gui_main import SecureScanGUI
        print("Starting SecureScan GUI...")
        app = SecureScanGUI()
        app.run()
    except ImportError as e:
        print(f"Error importing GUI modules: {e}")
        print("\nMake sure all these files are in the same directory:")
        print("  - gui_main.py")
        print("  - gui_port_scanner.py")
        print("  - gui_vulnerability_checker.py")
        print("  - gui_report_generator.py")
        print("  - gui_utils.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error running GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()