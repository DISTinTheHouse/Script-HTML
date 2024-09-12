import http.server
import socketserver
import socket
from datetime import datetime
import requests
import json

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

    def do_POST(self):
        if self.path == '/location':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = (
                f"Timestamp: {timestamp}\n"
                f"Latitud: {latitude}\n"
                f"Longitud: {longitude}\n"
                "----------------------------------------\n"
            )
            
            # Registra coordenadas en el archivo .txt
            with open("access_log.txt", "a") as log_file:
                log_file.write(log_entry)
            
            # Responde al cliente
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response_message = 'Ubicación recibida y registrada'
            self.wfile.write(response_message.encode('utf-8'))  
        else:
            super().do_POST()

# Obtén la IP local
local_ip = get_local_ip()

# Configura el servidor HTTP
with socketserver.TCPServer((local_ip, PORT), CustomHandler) as httpd:
    print(f"Sirviendo en http://{local_ip}:{PORT}")
    print("Presiona Ctrl+C para detener el servidor.")
    # Ejecuta el servidor hasta que lo detengas manualmente
    httpd.serve_forever()


##ALTA CALIBRAR ip PERSONAL Y PUBLICA
# FALTA AGREGAR VIDEO YOUTUBE

##FORMATO PARA HTML Y SERVIDOR:
# import socket
# import requests
# from datetime import datetime
# from django.shortcuts import render

# # Función para obtener la IP local
# def get_local_ip():
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
#     return local_ip

# # Función para obtener la IP pública
# def get_public_ip():
#     try:
#         response = requests.get('https://api.ipify.org?format=json')
#         ip_data = response.json()
#         return ip_data['ip']
#     except requests.RequestException as e:
#         print(f"Error al obtener IP pública: {e}")
#         return None

# # Vista test8 que se ejecuta al acceder a la URL (sin método POST)
# def test8(request):
#     # Obtener IP local y pública
#     client_ip = get_local_ip()
#     public_ip = get_public_ip()

#     # Obtener información del cliente desde los headers
#     user_agent = request.headers.get('User-Agent', 'Desconocido')
#     accept_language = request.headers.get('Accept-Language', 'Desconocido')
#     timezone = request.headers.get('Time-Zone', 'Desconocido')

#     # Timestamp de la solicitud
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     # Registrar la información en un archivo de texto
#     log_entry = (
#         f"Timestamp: {timestamp}\n"
#         f"IP Local: {client_ip}\n"
#         f"IP Pública: {public_ip}\n"
#         f"User-Agent: {user_agent}\n"
#         f"Accept-Language: {accept_language}\n"
#         f"Time-Zone: {timezone}\n"
#         "----------------------------------------\n"
#     )

#     with open("access_log.txt", "a") as log_file:
#         log_file.write(log_entry)

#     # Renderizar la página HTML
#     return render(request, 'calidad/calidad.html')
