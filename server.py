import http.server
import socketserver
import socket
from datetime import datetime
import requests

def print_ascii_art():
    ascii_art = """
          _____
       .-'     `-.
     .'           `.
    /   _.._   _.._   \\
   |   /    \\ /    \\   |
   |   \\    / \\    /   |
    \\   `--'   `--'   /
     `.           .'
       `-._   _.-'
           `"`
    Creado por DST
    GitHub: https://github.com/DISTinTheHouse
    License: MIT
    """
    print(ascii_art)

print_ascii_art()

PORT = 8000

# Detecta auto IP local
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

# IP Pública
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        print(f"Error al obtener IP pública: {e}")
        return None

# Establece la carpeta en la que estás sirviendo los archivos (en este caso, la misma que el script)
DIRECTORY = "."

# Crea un manejador que sirva los archivos HTML, CSS, JS en la carpeta actual
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        client_ip = self.client_address[0]
        public_ip = get_public_ip()
        user_agent = self.headers.get('User-Agent', 'Desconocido')
        accept_language = self.headers.get('Accept-Language', 'Desconocido')
        timezone = self.headers.get('Time-Zone', 'Desconocido')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = (
            f"Timestamp: {timestamp}\n"
            f"IP: {client_ip}\n"
            f"IP Pública: {public_ip}\n"
            f"usuario-agente: {user_agent}\n"
            f"Accept-Language: {accept_language}\n"
            f"Time-Zone: {timezone}\n"
            "----------------------------------------\n"
        )
        
        # Registra detalles en un archivo .txt
        with open("access_log.txt", "a") as log_file:
            log_file.write(log_entry)
        
        # Y en consola
        print(log_entry)

# Obtén la IP local
local_ip = get_local_ip()

# Configura el servidor HTTP
with socketserver.TCPServer((local_ip, PORT), CustomHandler) as httpd:
    print(f"Sirviendo en http://{local_ip}:{PORT}")
    print("Presiona Ctrl+C para detener el servidor.")
    # Ejecuta el servidor hasta que lo detengas manualmente
    httpd.serve_forever()
