"""
Start multiple vulnerable services on different ports
"""
import threading
import subprocess
import sys

def start_http_vuln():
    """Start vulnerable HTTP server"""
    import vulnerable_server
    vulnerable_server.start_vulnerable_server(8080)

def start_ftp_vuln():
    """Start vulnerable FTP server"""
    try:
        from pyftpdlib.servers import FTPServer
        start_ftp_vuln()
    except ImportError:
        print("FTP server requires: pip install pyftpdlib")

def start_telnet_vuln():
    """Start vulnerable telnet server"""
    import socket
    import threading
    
    def handle_client(conn, addr):
        conn.send(b"Welcome to vulnerable telnet server\r\n")
        conn.send(b"Login: ")
        user = conn.recv(1024).decode().strip()
        conn.send(b"Password: ")
        password = conn.recv(1024).decode().strip()
        
        # ANY username/password works (vulnerable!)
        conn.send(b"\r\nAccess granted!\r\n")
        conn.send(f"Hello {user}, you're in a vulnerable system!\r\n".encode())
        conn.close()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 23))
    server.listen(5)
    print("Telnet server running on port 23 (no auth required!)")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def start_mysql_vuln():
    """Start vulnerable MySQL (requires Docker)"""
    print("""
    To start vulnerable MySQL:
    docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql:5.7
    """)

if __name__ == "__main__":
    print("Starting vulnerable services...")
    print("=" * 50)
    
    # Start HTTP vulnerable server
    http_thread = threading.Thread(target=start_http_vuln, daemon=True)
    http_thread.start()
    
    # Start telnet server
    telnet_thread = threading.Thread(target=start_telnet_vuln, daemon=True)
    telnet_thread.start()
    
    print("\nServices running. Use Ctrl+C to stop.\n")
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")