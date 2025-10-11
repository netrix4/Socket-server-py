import socket
import json
from DTOs.UserAuthResponse import UserAuthResponse

# HOST = '192.168.0.190'
# HOST = '0.0.0.0'

CHARFORMAT = 'utf-8'
HOST = '192.168.0.124'
PORT = 555

def read_credentials()->str:
  username = input('Ingresa tu usuario: ')
  passWord = input('Ingresa tu contrasena: ')

  return json.dumps({'username':username, 'password':passWord})

def translate_server_response(user_response) -> UserAuthResponse:
  response = json.loads(user_response.decode(CHARFORMAT))

  return UserAuthResponse(status=response["status"], 
                          message=response["message"],
                          user_id=["user_id"])

def start_client():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Conectado al servidor en {HOST}:{PORT}")

    json_stringed = read_credentials()
    s.sendall(json_stringed.encode(CHARFORMAT))

    binary_user_response = s.recv(1824)
    newUserAuthResponse = translate_server_response(binary_user_response)

    print(f'Mensaje recibido del servidor: {newUserAuthResponse.message}')

    while newUserAuthResponse.status == 200:
      command = input("Dame un comando a mandar:")
      s.sendall(command.encode(CHARFORMAT))

      if command == 'quit':
        print('cerrado localmente')
        # newUserAuthResponse = UserAuthResponse(message='', status=0, user_id=0)
        s.close()
        break
      else:
        command_output_response = s.recv(1024).decode(CHARFORMAT)
        print(f"Esta fue la salida de tu comando:\n{command_output_response}")
    print('Parece que se cerro la conexion')
    s.close()


if __name__ == '__main__':
  start_client()