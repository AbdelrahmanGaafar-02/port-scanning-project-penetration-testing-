"""
SecureScan GUI - Educational Vulnerability Scanner with Graphical Interface
For authorized testing only!
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
from datetime import datetime
import os
import json

# Import scanner modules
from gui_port_scanner import GUIPortScanner
from gui_vulnerability_checker import GUIVulnerabilityChecker
from gui_report_generator import GUIReportGenerator
from gui_utils import GUILogger, Colors

class SecureScanGUI:
    """Main GUI Application Class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SecureScan - Educational Vulnerability Scanner")
        self.root.geometry("1200x700")
        self.root.minsize(900, 500)
        
        # Set icon if available
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Scanner state
        self.scanning = False
        self.current_scan_thread = None
        self.results = {}
        
        # Setup GUI
        self.setup_styles()
        self.create_menu()
        self.create_main_layout()
        
        # Logger for output
        self.logger = GUILogger(self.output_text)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Courier', 10))
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Target List", command=self.load_targets)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Scan Menu
        scan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Scan", menu=scan_menu)
        scan_menu.add_command(label="Quick Scan", command=self.start_quick_scan)
        scan_menu.add_command(label="Full Scan", command=self.start_full_scan)
        scan_menu.add_command(label="Port Scan Only", command=self.start_port_scan)
        scan_menu.add_command(label="Web Vuln Scan Only", command=self.start_web_scan)
        scan_menu.add_separator()
        scan_menu.add_command(label="Stop Scan", command=self.stop_scan)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Legal Notice", command=self.show_legal)
        
    def create_main_layout(self):
        """Create main application layout"""
        # Main container with paned windows
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left Panel - Configuration
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Right Panel - Results
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        self.create_config_panel(left_frame)
        self.create_results_panel(right_frame)
        
    def create_config_panel(self, parent):
        """Create configuration panel on the left"""
        # Target Configuration
        target_frame = ttk.LabelFrame(parent, text="Target Configuration", padding=10)
        target_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(target_frame, text="Target URL/IP:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.target_entry = ttk.Entry(target_frame, width=30)
        self.target_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.target_entry.insert(0, "http://localhost:8080")
        
        ttk.Label(target_frame, text="Ports (comma separated):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ports_entry = ttk.Entry(target_frame, width=30)
        self.ports_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.ports_entry.insert(0, "21,22,23,25,53,80,110,143,443,8080,3306,3389,5432,8443")
        
        # Scan Options
        options_frame = ttk.LabelFrame(parent, text="Scan Options", padding=10)
        options_frame.pack(fill=tk.X, pady=5)
        
        self.port_scan_var = tk.BooleanVar(value=True)
        self.web_vuln_var = tk.BooleanVar(value=True)
        self.save_report_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Port Scan", variable=self.port_scan_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Web Vulnerability Scan", variable=self.web_vuln_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Save Report", variable=self.save_report_var).pack(anchor=tk.W, pady=2)
        
        # Common Targets
        targets_frame = ttk.LabelFrame(parent, text="Quick Targets", padding=10)
        targets_frame.pack(fill=tk.X, pady=5)
        
        quick_targets = [
            ("localhost", "http://localhost:8080"),
            ("Test Target", "http://localhost:8888"),
            ("Local IP", "192.168.1.1"),
        ]
        
        for name, target in quick_targets:
            ttk.Button(targets_frame, text=name, 
                      command=lambda t=target: self.target_entry.delete(0, tk.END) or self.target_entry.insert(0, t)
                      ).pack(fill=tk.X, pady=2)
        
        # Control Buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.scan_button = ttk.Button(control_frame, text="▶ Start Scan", command=self.start_full_scan)
        self.scan_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.stop_button = ttk.Button(control_frame, text="⏹ Stop Scan", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        clear_button = ttk.Button(control_frame, text="🗑 Clear Output", command=self.clear_output)
        clear_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10,0))
        
    def create_results_panel(self, parent):
        """Create results panel on the right"""
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Output Tab
        output_frame = ttk.Frame(self.notebook)
        self.notebook.add(output_frame, text="📋 Scan Output")
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colors
        self.output_text.tag_config('info', foreground='blue')
        self.output_text.tag_config('success', foreground='green')
        self.output_text.tag_config('warning', foreground='orange')
        self.output_text.tag_config('error', foreground='red')
        self.output_text.tag_config('title', foreground='purple', font=('Arial', 12, 'bold'))
        
        # Results Tab
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="📊 Scan Results")
        
        # Tree view for results
        self.results_tree = ttk.Treeview(results_frame, columns=('Type', 'Finding', 'Severity'), show='tree headings')
        self.results_tree.heading('#0', text='#')
        self.results_tree.heading('Type', text='Type')
        self.results_tree.heading('Finding', text='Finding')
        self.results_tree.heading('Severity', text='Severity')
        
        # Configure column widths
        self.results_tree.column('#0', width=50)
        self.results_tree.column('Type', width=120)
        self.results_tree.column('Finding', width=400)
        self.results_tree.column('Severity', width=100)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Open Ports Tab
        ports_frame = ttk.Frame(self.notebook)
        self.notebook.add(ports_frame, text="🔌 Open Ports")
        
        self.ports_tree = ttk.Treeview(ports_frame, columns=('Port', 'Service', 'Status'), show='headings')
        self.ports_tree.heading('Port', text='Port')
        self.ports_tree.heading('Service', text='Service')
        self.ports_tree.heading('Status', text='Status')
        
        self.ports_tree.column('Port', width=100)
        self.ports_tree.column('Service', width=200)
        self.ports_tree.column('Status', width=100)
        
        ports_scrollbar = ttk.Scrollbar(ports_frame, orient=tk.VERTICAL, command=self.ports_tree.yview)
        self.ports_tree.configure(yscrollcommand=ports_scrollbar.set)
        
        self.ports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ports_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Vulnerabilities Tab
        vuln_frame = ttk.Frame(self.notebook)
        self.notebook.add(vuln_frame, text="⚠ Vulnerabilities")
        
        self.vuln_tree = ttk.Treeview(vuln_frame, columns=('Severity', 'Description', 'Location'), show='headings')
        self.vuln_tree.heading('Severity', text='Severity')
        self.vuln_tree.heading('Description', text='Description')
        self.vuln_tree.heading('Location', text='Location')
        
        self.vuln_tree.column('Severity', width=100)
        self.vuln_tree.column('Description', width=400)
        self.vuln_tree.column('Location', width=200)
        
        vuln_scrollbar = ttk.Scrollbar(vuln_frame, orient=tk.VERTICAL, command=self.vuln_tree.yview)
        self.vuln_tree.configure(yscrollcommand=vuln_scrollbar.set)
        
        self.vuln_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vuln_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def log(self, message, level='info'):
        """Add message to output with color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        self.output_text.insert(tk.END, formatted_msg, level)
        self.output_text.see(tk.END)
        
        # Also print to console for debugging
        print(formatted_msg.strip())
        
    def clear_output(self):
        """Clear the output text widget"""
        self.output_text.delete(1.0, tk.END)
        self.results_tree.delete(*self.results_tree.get_children())
        self.ports_tree.delete(*self.ports_tree.get_children())
        self.vuln_tree.delete(*self.vuln_tree.get_children())
        
    def update_results_tree(self, results):
        """Update the results tree view"""
        # Clear existing
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add port scan results
        if 'ports' in results:
            open_ports = [p for p in results['ports'] if p.get('status') == 'open']
            self.results_tree.insert('', 'end', text=str(len(open_ports)), 
                                     values=('Port Scan', f'Found {len(open_ports)} open ports', 'Info'))
            
            # Update ports tab
            for port in results['ports']:
                self.ports_tree.insert('', 'end', values=(port['port'], port.get('service', 'Unknown'), port['status']))
        
        # Add vulnerability results
        if 'vulnerabilities' in results:
            for vuln in results['vulnerabilities']:
                self.results_tree.insert('', 'end', text='', 
                                         values=('Vulnerability', vuln.get('description', ''), vuln.get('severity', 'Unknown')))
                
                # Update vuln tab
                self.vuln_tree.insert('', 'end', values=(vuln.get('severity', 'Medium'), 
                                                        vuln.get('description', ''), 
                                                        vuln.get('location', self.target_entry.get())))
        
    def stop_scan(self):
        """Stop the current scan"""
        self.scanning = False
        self.log("Scan stopped by user", 'warning')
        self.status_var.set("Scan stopped")
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
    def start_quick_scan(self):
        """Start a quick scan (common ports only)"""
        if not self.validate_target():
            return
        
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning = True
        
        self.current_scan_thread = threading.Thread(target=self.run_quick_scan)
        self.current_scan_thread.daemon = True
        self.current_scan_thread.start()
        
    def start_full_scan(self):
        """Start a full scan"""
        if not self.validate_target():
            return
        
        self.clear_output()
        self.log("=" * 60, 'title')
        self.log("SECURESCAN - Starting Full Security Scan", 'title')
        self.log("=" * 60, 'title')
        self.log(f"Target: {self.target_entry.get()}", 'info')
        
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning = True
        self.status_var.set("Scanning...")
        
        self.current_scan_thread = threading.Thread(target=self.run_full_scan)
        self.current_scan_thread.daemon = True
        self.current_scan_thread.start()
        
    def start_port_scan(self):
        """Run port scan only"""
        if not self.validate_target():
            return
        
        self.clear_output()
        self.log("Starting Port Scan Only...", 'info')
        
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning = True
        
        self.current_scan_thread = threading.Thread(target=self.run_port_scan_only)
        self.current_scan_thread.daemon = True
        self.current_scan_thread.start()
        
    def start_web_scan(self):
        """Run web vulnerability scan only"""
        if not self.validate_target():
            return
        
        self.clear_output()
        self.log("Starting Web Vulnerability Scan Only...", 'info')
        
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning = True
        
        self.current_scan_thread = threading.Thread(target=self.run_web_scan_only)
        self.current_scan_thread.daemon = True
        self.current_scan_thread.start()
        
    def validate_target(self):
        """Validate target input"""
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target URL or IP address")
            return False
        return True
        
    def parse_ports(self):
        """Parse ports from entry field"""
        ports_text = self.ports_entry.get().strip()
        if ports_text:
            try:
                return [int(p.strip()) for p in ports_text.split(',') if p.strip()]
            except ValueError:
                self.log("Invalid port format, using defaults", 'warning')
        return None
        
    def run_quick_scan(self):
        """Run quick scan in background thread"""
        try:
            target = self.target_entry.get()
            
            # Quick port scan on common ports
            self.log("\n--- Quick Port Scan ---", 'title')
            scanner = GUIPortScanner(target, self.log)
            port_results = scanner.scan_all_ports()
            
            if port_results and not self.scanning:
                return
                
            self.results['ports'] = port_results
            
            # Quick web check if target is HTTP
            if target.startswith(('http://', 'https://')):
                self.log("\n--- Quick Web Check ---", 'title')
                vuln_checker = GUIVulnerabilityChecker(target, self.log)
                vuln_results = vuln_checker.run_all_checks()
                self.results['vulnerabilities'] = vuln_results
            
            # Update UI
            self.root.after(0, self.scan_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Scan error: {e}", 'error'))
            self.root.after(0, self.scan_complete)
            
    def run_full_scan(self):
        """Run full scan in background thread"""
        try:
            target = self.target_entry.get()
            ports = self.parse_ports()
            
            # Port Scan
            if self.port_scan_var.get() and self.scanning:
                self.root.after(0, lambda: self.log("\n" + "="*40, 'title'))
                self.root.after(0, lambda: self.log("PHASE 1: PORT SCANNING", 'title'))
                self.root.after(0, lambda: self.log("="*40, 'title'))
                
                scanner = GUIPortScanner(target, self.log, ports)
                port_results = scanner.scan_all_ports()
                
                if not self.scanning:
                    return
                    
                self.results['ports'] = port_results
                open_count = len([p for p in port_results if p['status'] == 'open'])
                self.root.after(0, lambda: self.log(f"Port scan complete. Found {open_count} open ports.", 'success'))
            
            # Web Vulnerability Scan
            if self.web_vuln_var.get() and self.scanning and target.startswith(('http://', 'https://')):
                self.root.after(0, lambda: self.log("\n" + "="*40, 'title'))
                self.root.after(0, lambda: self.log("PHASE 2: VULNERABILITY ASSESSMENT", 'title'))
                self.root.after(0, lambda: self.log("="*40, 'title'))
                
                vuln_checker = GUIVulnerabilityChecker(target, self.log)
                vuln_results = vuln_checker.run_all_checks()
                
                if not self.scanning:
                    return
                    
                self.results['vulnerabilities'] = vuln_results
            
            # Save Report
            if self.save_report_var.get() and self.results:
                self.root.after(0, lambda: self.log("\n--- Generating Report ---", 'title'))
                report_gen = GUIReportGenerator(target, self.results, self.log)
                report_paths = report_gen.generate_reports()
                self.root.after(0, lambda: self.log(f"Reports saved: {', '.join(report_paths)}", 'success'))
            
            self.root.after(0, self.scan_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Scan error: {e}", 'error'))
            self.root.after(0, self.scan_complete)
            
    def run_port_scan_only(self):
        """Run only port scan"""
        try:
            target = self.target_entry.get()
            ports = self.parse_ports()
            
            scanner = GUIPortScanner(target, self.log, ports)
            port_results = scanner.scan_all_ports()
            
            if self.scanning:
                self.results['ports'] = port_results
                
                if self.save_report_var.get():
                    report_gen = GUIReportGenerator(target, self.results, self.log)
                    report_gen.generate_reports()
            
            self.root.after(0, self.scan_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Scan error: {e}", 'error'))
            self.root.after(0, self.scan_complete)
            
    def run_web_scan_only(self):
        """Run only web vulnerability scan"""
        try:
            target = self.target_entry.get()
            
            if not target.startswith(('http://', 'https://')):
                self.root.after(0, lambda: self.log("Web scan requires HTTP/HTTPS URL", 'error'))
                self.root.after(0, self.scan_complete)
                return
            
            vuln_checker = GUIVulnerabilityChecker(target, self.log)
            vuln_results = vuln_checker.run_all_checks()
            
            if self.scanning:
                self.results['vulnerabilities'] = vuln_results
                
                if self.save_report_var.get():
                    report_gen = GUIReportGenerator(target, self.results, self.log)
                    report_gen.generate_reports()
            
            self.root.after(0, self.scan_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Scan error: {e}", 'error'))
            self.root.after(0, self.scan_complete)
            
    def scan_complete(self):
        """Handle scan completion"""
        self.scanning = False
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Update results tree
        if self.results:
            self.update_results_tree(self.results)
        
        self.log("\n" + "="*60, 'title')
        self.log("SCAN COMPLETED SUCCESSFULLY", 'success')
        self.log("="*60, 'title')
        
        self.status_var.set("Ready")
        
    def load_targets(self):
        """Load targets from file"""
        filename = filedialog.askopenfilename(
            title="Load Target List",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    targets = f.read().strip().split('\n')
                if targets:
                    self.target_entry.delete(0, tk.END)
                    self.target_entry.insert(0, targets[0])
                    self.log(f"Loaded {len(targets)} targets from {filename}", 'info')
            except Exception as e:
                self.log(f"Error loading targets: {e}", 'error')
                
    def save_results(self):
        """Save scan results to file"""
        if not self.results:
            messagebox.showwarning("No Results", "No scan results to save. Run a scan first.")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(self.results, f, indent=4)
                else:
                    with open(filename, 'w') as f:
                        f.write(f"SecureScan Results\n")
                        f.write(f"Target: {self.target_entry.get()}\n")
                        f.write(f"Date: {datetime.now()}\n")
                        f.write(f"\nResults:\n{json.dumps(self.results, indent=2)}")
                
                self.log(f"Results saved to {filename}", 'success')
            except Exception as e:
                self.log(f"Error saving results: {e}", 'error')
                
    def show_about(self):
        """Show about dialog"""
        about_text = """SecureScan GUI v2.0
Educational Vulnerability Scanner

A graphical tool for learning about security scanning.

Features:
• Port scanning
• Web vulnerability assessment
• Security headers analysis
• Report generation

FOR EDUCATIONAL PURPOSES ONLY!
Only scan systems you own or have permission to test."""
        
        messagebox.showinfo("About SecureScan", about_text)
        
    def show_legal(self):
        """Show legal notice"""
        legal_text = """⚠️ LEGAL NOTICE ⚠️

This tool is for EDUCATIONAL PURPOSES only.

Unauthorized scanning of computer systems is ILLEGAL in most jurisdictions.

By using this tool, you agree to:
1. Only scan systems you OWN
2. Only scan systems you have EXPLICIT WRITTEN PERMISSION to test
3. Use this software responsibly and ethically

The author assumes NO LIABILITY for misuse of this software."""
        
        messagebox.showwarning("Legal Notice", legal_text)
        
    def on_closing(self):
        """Handle window close event"""
        if self.scanning:
            if messagebox.askyesno("Scan in Progress", "A scan is currently running. Stop and exit?"):
                self.scanning = False
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = SecureScanGUI()
    app.run()