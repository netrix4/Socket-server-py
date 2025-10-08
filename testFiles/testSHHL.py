import paramiko
import socket
import sys
import threading
import os
# Importaciones de tus módulos (DTOs, SQLiteProvider, etc.)
from DTOs.UserAuthResponse import UserAuthResponse
from service.SQLiteProvider import SQLiteProvider 

HOST = '192.168.0.226'
PORT = 555
CHARFORMAT = 'utf-8'
HOST_KEY = paramiko.RSAKey.generate(2048) # DEBES USAR UNA CLAVE PERSISTENTE EN PRODUCCIÓN

SQLiteConnection = SQLiteProvider('SocketUsers.db')

def get_is_valid_user(userToLoginAsTuple) -> UserAuthResponse:
  # Tu función de validación permanece igual
  return SQLiteProvider.isValidUser(self=SQLiteConnection, user=userToLoginAsTuple)

# --- Clases de Paramiko para Manejar Sesiones y Autenticación ---

class Server(paramiko.ServerInterface):
    """
    Clase que implementa el manejo de sesiones y autenticación SSH.
    """
    def __init__(self):
        self.event = threading.Event()
    
    def check_auth_password(self, username, password):
        """
        Sobreescribe el método de Paramiko para usar tu lógica de validación.
        """
        user_credentials = (username, password)
        user_validation_response = get_is_valid_user(user_credentials)
        
        if user_validation_response.status == 200:
            print(f"Usuario {username} autenticado con éxito.")
            # Retorna paramiko.AUTH_SUCCESSFUL si la autenticación es válida
            return paramiko.AUTH_SUCCESSFUL
        else:
            print(f"Fallo de autenticación para {username}.")
            # Retorna paramiko.AUTH_FAILED si falla
            return paramiko.AUTH_FAILED
    
    def check_channel_request(self, kind, chanid):
        # Acepta solicitudes de sesión estándar
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel, command):
        """
        Sobreescribe para ejecutar el comando del cliente (con el parámetro opcional)
        """
        print(f'Comando SSH a ejecutar: -> {command.decode(CHARFORMAT)} <-')
        
        try:
            # Ejecuta el comando en el SO y envía la salida de vuelta
            output = os.popen(command.decode(CHARFORMAT)).read()
            channel.sendall(output.encode(CHARFORMAT))
            channel.sendall(b'\n') # Asegura un salto de línea
            channel.close()
            return True
        except Exception as e:
            channel.sendall(f"Error en ejecución: {e}".encode(CHARFORMAT))
            channel.close()
            return False

# --- Función Principal del Servidor ---

def start_ssh_server():
    """
    Inicia el servidor SSH escuchando conexiones.
    """
    print(f"Iniciando servidor SSH en {HOST}:{PORT}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
    except Exception as e:
        print(f'*** Fallo al enlazar el socket: {e}')
        sys.exit(1)

    try:
        sock.listen(100)
        print('Escuchando por conexiones...')
    except Exception as e:
        print(f'*** Fallo al escuchar: {e}')
        sys.exit(1)

    while True:
        try:
            conn, addr = sock.accept()
        except Exception as e:
            print(f'*** Fallo en accept(): {e}')
            continue

        # Inicia un hilo para manejar cada conexión SSH
        t = threading.Thread(target=handle_ssh_connection, args=(conn, addr))
        t.start()

def handle_ssh_connection(conn, addr):
    """
    Maneja el protocolo SSH para una conexión individual.
    """
    print(f'Conexión SSH entrante de {addr}')
    try:
        # 1. Configurar y negociar la conexión SSH
        transport = paramiko.Transport(conn)
        transport.add_server_key(HOST_KEY)
        server = Server()
        transport.start_server(server=server)

        # 2. Esperar el canal (el túnel de comunicación)
        channel = transport.accept(20) # Espera 20 segundos
        
        if channel is None:
            print('***No se pudo abrir el canal.')
            transport.close()
            return
            
        print('Canal abierto. Listo para comandos.')
        
        # En este punto, la lógica de Paramiko espera la solicitud 'exec' del cliente
        # y la dirige a check_channel_exec_request en la clase Server.

        # NOTA: Para sesiones interactivas (sin comandos opcionales),
        # se necesitaría implementar 'check_channel_shell_request' y un loop interactivo.

        while transport.is_active():
            # Mantiene el hilo vivo mientras la conexión esté activa
            paramiko.time.sleep(1)

    except Exception as e:
        print(f'*** Excepción durante la conexión SSH de {addr}: {e}')
    finally:
        try:
            transport.close()
        except:
            pass
        print(f'Conexión SSH con {addr} terminada.')


if __name__ == '__main__':
    start_ssh_server() 
