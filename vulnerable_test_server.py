"""
Simple Vulnerable Test Server for Educational Purposes
Opens port 8888 with intentional vulnerabilities for scanner testing
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

class VulnerableHandler(SimpleHTTPRequestHandler):
    """Handler with intentional security vulnerabilities"""
    
    def do_GET(self):
        """Handle GET requests with vulnerabilities"""
        
        # ============================================
        # VULNERABILITY 1: Sensitive file exposure
        # ============================================
        if self.path == '/.env':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"""
DB_PASSWORD=admin123
API_KEY=sk_test_4eC39HqLyjWDarjtT1zdp7dc
SECRET_KEY=mysecretkey12345
            """.strip())
            return
        
        # ============================================
        # VULNERABILITY 2: Admin panel exposed
        # ============================================
        if self.path == '/admin':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <body>
                <h1>Admin Panel</h1>
                <p>Username: admin</p>
                <p>Password: password123</p>
                <p>Database: localhost:3306</p>
            </body>
            </html>
            """)
            return
        
        # ============================================
        # VULNERABILITY 3: XSS (Cross-Site Scripting)
        # ============================================
        if self.path.startswith('/search'):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            query = params.get('q', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # INTENTIONAL: No input sanitization - XSS vulnerability!
            html = f"""
            <html>
            <body>
                <h1>Search Results</h1>
                <p>You searched for: {query}</p>
                <p>Try: /search?q=<script>alert('XSS')</script></p>
                <form>
                    <input type="text" name="q" placeholder="Search...">
                    <input type="submit">
                </form>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
        
        # ============================================
        # VULNERABILITY 4: Missing security headers
        # ============================================
        # Intentionally NOT adding security headers!
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        # Intentionally exposing server info
        self.send_header('Server', 'Apache/2.4.41 (Ubuntu)')
        self.send_header('X-Powered-By', 'PHP/7.4.3')
        # MISSING: X-Frame-Options, CSP, HSTS, etc.
        self.end_headers()
        
        # Main page (using string, not bytes directly to avoid encoding issues)
        html_content = """
        <html>
        <head><title>Vulnerable Test Server</title></head>
        <body>
            <h1>[!] Vulnerable Test Server</h1>
            <p>This server has intentional vulnerabilities for testing!</p>
            
            <h2>Try these vulnerable endpoints:</h2>
            <ul>
                <li><a href="/.env">Exposed .env file</a></li>
                <li><a href="/admin">Exposed admin panel</a></li>
                <li><a href="/search?q=test">XSS vulnerable search</a></li>
                <li><a href="/search?q=<script>alert('XSS')</script>">Test XSS</a></li>
            </ul>
            
            <h3>What your scanner will detect:</h3>
            <ul>
                <li>Open port detection</li>
                <li>Exposed sensitive files</li>
                <li>Missing security headers</li>
                <li>Server info disclosure</li>
                <li>Potential XSS vulnerabilities</li>
            </ul>
            
            <hr>
            <p style="color:red"><strong>WARNING: EDUCATIONAL PURPOSE ONLY - DO NOT DEPLOY TO PRODUCTION!</strong></p>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
    
    def log_message(self, format, *args):
        """Log requests with simple formatting"""
        print(f"[ACCESS] {format % args}")

def run_server(port=8888):
    """Start the vulnerable test server"""
    server = HTTPServer(('localhost', port), VulnerableHandler)
    print(f"""
============================================
     VULNERABLE TEST SERVER RUNNING
============================================
  Port: {port}
  URL:  http://localhost:{port}

  Vulnerabilities for scanner to detect:
  - Exposed sensitive files (/.env, /admin)
  - Missing security headers
  - Server information disclosure
  - XSS vulnerability on /search

  Press Ctrl+C to stop
============================================
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[!] Shutting down server...")
        server.shutdown()

if __name__ == "__main__":
    run_server(8888)