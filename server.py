import socket
import os
import json
from DTOs.UserAuthResponse import UserAuthResponse
from service.SQLiteProvider import SQLiteProvider

# HOST = '192.168.0.190'
# HOST = '0.0.0.0'
CHARFORMAT = 'utf-8'
HOST = '192.168.0.124'
PORT = 555

SQLiteConnection = SQLiteProvider('SocketUsers.db')

def get_is_valid_user(userToLoginAsTuple)->UserAuthResponse:
  return SQLiteProvider.isValidUser(self=SQLiteConnection, user=userToLoginAsTuple)

def translate_client_response(userToLogin):
  userToLoginAsJSON = json.loads(userToLogin.decode(CHARFORMAT))
  return (userToLoginAsJSON["username"], userToLoginAsJSON["password"])

def setup_socket(socketServer):
  socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  socketServer.bind((HOST, PORT))
  socketServer.listen(2)
  # socketServer.setblocking(False)
  print(f"Servidor escuchando en {HOST}:{PORT}")
  return socketServer.accept()  


def start_server():
  isallowedconnection = True
  # while True:
      # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    conn, addr = setup_socket(s)

    with conn:
      user_credentials = translate_client_response(conn.recv(1024))
      user_validation_response = get_is_valid_user(user_credentials)

      if user_validation_response.status == 200:
        print(f'Bienvenido, {user_credentials[0]}')
        print(f"Conectado por {addr}")

        conn.sendall(json.dumps(user_validation_response.to_dict()).encode(CHARFORMAT))

        print('Escuchando clientes...')

        while isallowedconnection:
          data = conn.recv(1024).decode(CHARFORMAT)
          if not data:
            print('Creo que aqui se cierra cuando el host se desconecta')
            conn.close()
            break
          else:
            if data == 'quit':
              print('Cerrando conexion por peticion del cliente')
              conn.close()
              isallowedconnection = not isallowedconnection
              break
            else:
              print(f'Comando a ejecutar: -> {data} <-')
              try:
                output = os.popen(data).read()
                if output:
                  conn.sendall(output.encode(CHARFORMAT))
                else:
                  conn.sendall(b"-- Comando sin salida --")
              except Exception as e:
                  conn.sendall(f"Error: {e}".encode(CHARFORMAT))

      else:
        # ToDo: Ask for create new user
        user_validation_response = json.dumps(user_validation_response.to_dict())
        print('Parece que tu usuario no existe', user_validation_response)
        conn.sendall(user_validation_response.encode(CHARFORMAT))

      conn.close()
    conn.close()
    # break

if __name__ == '__main__':
  start_server()
