"""
GUI Report Generator Module
"""
import json
import os
from datetime import datetime

class GUIReportGenerator:
    """Report generator with GUI logging"""
    
    def __init__(self, target, results, log_callback):
        """
        Initialize report generator
        
        Args:
            target: Target that was scanned
            results: Scan results dictionary
            log_callback: Logging function
        """
        self.target = target
        self.results = results
        self.log = log_callback
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists('scan_reports'):
            os.makedirs('scan_reports')
            self.log("Created scan_reports directory", 'info')
            
    def generate_text_report(self):
        """Generate text format report"""
        self.ensure_output_dir()
        filename = f"scan_reports/report_{self.timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("SECURESCAN - VULNERABILITY ASSESSMENT REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Target: {self.target}\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Report ID: {self.timestamp}\n\n")
            
            # Port Scan Results
            if 'ports' in self.results:
                f.write("-" * 50 + "\n")
                f.write("PORT SCAN RESULTS\n")
                f.write("-" * 50 + "\n")
                open_ports = [p for p in self.results['ports'] if p.get('status') == 'open']
                
                if open_ports:
                    f.write(f"Found {len(open_ports)} open ports:\n")
                    for port in open_ports:
                        f.write(f"  • Port {port['port']}: {port.get('service', 'Unknown')}\n")
                else:
                    f.write("No open ports found.\n")
                f.write("\n")
            
            # Vulnerability Results
            if 'vulnerabilities' in self.results and self.results['vulnerabilities']:
                f.write("-" * 50 + "\n")
                f.write("VULNERABILITY FINDINGS\n")
                f.write("-" * 50 + "\n")
                
                # Group by severity
                high = [v for v in self.results['vulnerabilities'] if v.get('severity') == 'High']
                medium = [v for v in self.results['vulnerabilities'] if v.get('severity') == 'Medium']
                low = [v for v in self.results['vulnerabilities'] if v.get('severity') == 'Low']
                
                if high:
                    f.write(f"\nHIGH SEVERITY ({len(high)}):\n")
                    for v in high:
                        f.write(f"  ⚠ {v['description']}\n")
                        f.write(f"    Location: {v.get('location', 'N/A')}\n")
                
                if medium:
                    f.write(f"\nMEDIUM SEVERITY ({len(medium)}):\n")
                    for v in medium:
                        f.write(f"  • {v['description']}\n")
                
                if low:
                    f.write(f"\nLOW SEVERITY ({len(low)}):\n")
                    for v in low:
                        f.write(f"  • {v['description']}\n")
            else:
                f.write("-" * 50 + "\n")
                f.write("VULNERABILITY FINDINGS\n")
                f.write("-" * 50 + "\n")
                f.write("No vulnerabilities found.\n")
            
            # Footer
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF REPORT - FOR EDUCATIONAL PURPOSES ONLY\n")
            f.write("=" * 70 + "\n")
        
        return filename
        
    def generate_json_report(self):
        """Generate JSON format report"""
        self.ensure_output_dir()
        filename = f"scan_reports/report_{self.timestamp}.json"
        
        report_data = {
            'scan_info': {
                'target': self.target,
                'timestamp': self.timestamp,
                'scan_date': datetime.now().isoformat(),
                'tool': 'SecureScan GUI v2.0'
            },
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4)
            
        return filename
        
    def generate_html_report(self):
        """Generate HTML format report"""
        self.ensure_output_dir()
        filename = f"scan_reports/report_{self.timestamp}.html"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>SecureScan Report - {self.target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: auto; background: white; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 25px; }}
        .high {{ background: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 10px 0; }}
        .medium {{ background: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 10px 0; }}
        .low {{ background: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 10px 0; }}
        .info {{ background: #e3f2fd; border-left: 4px solid #2196f3; padding: 10px; margin: 10px 0; }}
        .port {{ background: #f3e5f5; border-left: 4px solid #9c27b0; padding: 5px; margin: 5px 0; }}
        .footer {{ margin-top: 30px; text-align: center; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 SecureScan Vulnerability Assessment Report</h1>
        <p><strong>Target:</strong> {self.target}</p>
        <p><strong>Scan Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Report ID:</strong> {self.timestamp}</p>
"""
        
        # Port Results
        if 'ports' in self.results:
            html_content += """
        <h2>🔌 Port Scan Results</h2>
"""
            open_ports = [p for p in self.results['ports'] if p.get('status') == 'open']
            if open_ports:
                html_content += f"<p>Found {len(open_ports)} open ports:</p>"
                for port in open_ports:
                    html_content += f'<div class="port">Port {port["port"]}: {port.get("service", "Unknown")}</div>'
            else:
                html_content += "<p>No open ports found.</p>"
        
        # Vulnerability Results
        if 'vulnerabilities' in self.results and self.results['vulnerabilities']:
            html_content += """
        <h2>⚠ Vulnerability Findings</h2>
"""
            for vuln in self.results['vulnerabilities']:
                severity = vuln.get('severity', 'Medium').lower()
                html_content += f"""
        <div class="{severity}">
            <strong>{vuln.get('severity', 'Medium')}</strong>: {vuln.get('description', '')}
            <br><small>Location: {vuln.get('location', 'N/A')}</small>
        </div>
"""
        else:
            html_content += """
        <h2>⚠ Vulnerability Findings</h2>
        <div class="info">No vulnerabilities found.</div>
"""
        
        html_content += f"""
        <div class="footer">
            <p>Generated by SecureScan - Educational Vulnerability Scanner</p>
            <p>FOR EDUCATIONAL PURPOSES ONLY</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return filename
        
    def generate_reports(self):
        """Generate all report formats"""
        paths = []
        
        try:
            text_path = self.generate_text_report()
            paths.append(text_path)
            self.log(f"Text report saved: {text_path}", 'success')
        except Exception as e:
            self.log(f"Error generating text report: {e}", 'error')
            
        try:
            json_path = self.generate_json_report()
            paths.append(json_path)
            self.log(f"JSON report saved: {json_path}", 'success')
        except Exception as e:
            self.log(f"Error generating JSON report: {e}", 'error')
            
        try:
            html_path = self.generate_html_report()
            paths.append(html_path)
            self.log(f"HTML report saved: {html_path}", 'success')
        except Exception as e:
            self.log(f"Error generating HTML report: {e}", 'error')
            
        return paths