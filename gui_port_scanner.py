"""
GUI Port Scanner Module
"""
import socket
import threading
from datetime import datetime

class GUIPortScanner:
    """Port scanner with GUI logging support"""
    
    def __init__(self, target, log_callback, ports_to_scan=None):
        """
        Initialize scanner
        
        Args:
            target: IP or hostname to scan
            log_callback: Function to call for logging messages
            ports_to_scan: List of ports (optional)
        """
        self.target = self.extract_host(target)
        self.log = log_callback
        self.ports = ports_to_scan or [21, 22, 23, 25, 53, 80, 110, 143, 443, 445,
                                        3306, 3389, 5432, 8080, 8443]
        self.results = []
        self.stop_flag = False
        
    def extract_host(self, target):
        """Extract hostname from URL"""
        host = target.replace('http://', '').replace('https://', '')
        host = host.split('/')[0]
        host = host.split(':')[0]
        return host
        
    def scan_single_port(self, port):
        """Scan a single port"""
        if self.stop_flag:
            return False
            
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            sock.close()
            return result == 0
        except:
            return False
            
    def get_service_name(self, port):
        """Get common service name for port"""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 3306: 'MySQL', 3389: 'RDP',
            5432: 'PostgreSQL', 8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt'
        }
        return services.get(port, 'Unknown')
        
    def scan_all_ports(self):
        """Scan all configured ports"""
        self.log(f"Starting port scan on {self.target}", 'info')
        
        open_ports = []
        total = len(self.ports)
        
        for i, port in enumerate(self.ports):
            if self.stop_flag:
                break
                
            self.log(f"Checking port {port}... ({i+1}/{total})", 'info')
            
            if self.scan_single_port(port):
                service = self.get_service_name(port)
                self.log(f"✓ Port {port} is OPEN ({service})", 'success')
                open_ports.append({
                    'port': port,
                    'status': 'open',
                    'service': service
                })
            else:
                self.log(f"  Port {port}: closed", 'info')
        
        self.log(f"Port scan complete. Found {len(open_ports)} open ports.", 'success')
        return open_ports
        
    def stop(self):
        """Stop the scan"""
        self.stop_flag = True