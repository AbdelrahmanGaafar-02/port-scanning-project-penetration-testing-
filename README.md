Port Scanning project
# SecureScan GUI
**SecureScan GUI** is an Educational Vulnerability Scanner with a Graphical Interface. It is designed to help users learn the basics of port scanning, web vulnerability assessment, and security analysis in a safe, controlled environment.
⚠️ **LEGAL NOTICE**: This tool is for EDUCATIONAL PURPOSES only. Unauthorized scanning of computer systems is ILLEGAL. By using this tool, you agree to only scan systems you OWN or have EXPLICIT WRITTEN PERMISSION to test.
## Features
- **Port Scanning**: Scan common ports or specify custom ranges. Identifies open ports and commonly associated services (FTP, SSH, HTTP, MySQL, etc.).
- **Web Vulnerability Assessment**:
  - **Security Headers Check**: Detects missing critical security headers (X-Frame-Options, Content-Security-Policy, Strict-Transport-Security, etc.).
  - **Sensitive Files Exposure**: Checks for common exposed files (`/.env`, `/robots.txt`, `/backup/`, `/.git/config`, etc.).
  - **Server Information Disclosure**: Analyzes response headers to detect exposed server versions and technologies.
  - **Common Vulnerabilities**: Basic detection for common patterns like potential SQL injection points or XSS.
- **Report Generation**: Automatically generate and save detailed scan reports in JSON or Text format.
- **Vulnerable Test Server**: Includes a built-in vulnerable test server to practice scanning without targeting real systems.
## Prerequisites
- **Python 3.x**
- **Tkinter** (usually included with standard Python installations)
- **Dependencies**: `requests` (The launcher script will attempt to install missing dependencies automatically).
## Installation
1. Clone or download the repository to your local machine.
2. Navigate to the project directory.
## Usage
### Starting the Scanner
**On Windows:**
Simply double-click the `start_gui.bat` file. This will handle activating any virtual environment, installing dependencies, and launching the GUI.
**Using Python directly:**
Run the launcher script from your terminal:
```bash
python run_gui.py
```
This script automatically checks for required dependencies (like `requests` and `tkinter`) and launches the main application (`gui_main.py`).
### How to Scan
1. Open the SecureScan GUI.
2. In the **Target Configuration** panel, enter the Target URL or IP address (e.g., `http://localhost:8888`).
3. Specify the ports you want to scan (comma-separated).
4. Select your **Scan Options** (Port Scan, Web Vulnerability Scan, Save Report).
5. Click **▶ Start Scan**.
6. View real-time output in the **Scan Output** tab and review detailed findings in the **Scan Results**, **Open Ports**, and **Vulnerabilities** tabs.
### Practice with the Vulnerable Test Server
To safely test the scanner, you can run the included vulnerable test server. It intentionally hosts common vulnerabilities like exposed `.env` files, missing security headers, and an exposed admin panel.
1. Open a new terminal.
2. Run the test server:
   ```bash
   python vulnerable_test_server.py
   ```
3. The server will start on `http://localhost:8888`.
4. Point the SecureScan GUI to `http://localhost:8888` and start a full scan to see it detect the intentional vulnerabilities.
## Project Structure
- `gui_main.py` - Main Tkinter GUI application.
- `gui_port_scanner.py` - Module for performing port scans.
- `gui_vulnerability_checker.py` - Module for running web vulnerability checks.
- `gui_report_generator.py` - Module for saving scan results to files.
- `gui_utils.py` - Utilities for logging and formatting.
- `run_gui.py` - Launcher script that checks dependencies and starts the GUI.
- `start_gui.bat` - Windows batch script to launch the application easily.
- `vulnerable_test_server.py` - A simple vulnerable HTTP server for practice.
- `requirements_gui.txt` - Python package requirements.
- `scan_reports/` - Directory where generated scan reports are saved.
## Disclaimer
The author assumes NO LIABILITY for the misuse of this software. Always obtain permission before scanning any network or application.
