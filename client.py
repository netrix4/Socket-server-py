import socket
import json
from DTOs.UserAuthResponse import UserAuthResponse

# HOST = '192.168.0.190'
# HOST = '0.0.0.0'
HOST = '192.168.100.79'
PORT = 555

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Conectado al servidor en {HOST}:{PORT}")
    message = input('Usuario: ')
    s.sendall(message.encode('utf-8'))

    response = s.recv(1824).decode('utf-8')
    print(response)

    response = json.loads(response)

    print(f'Recibido del servidor: {response["message"]}')
    while response["status"] == 200:
      command = input("Dame un comando a mandar:")
      s.sendall(command.encode('utf-8'))
      if command == 'quit':
        print('cerrado localmente')
        response == ''
        s.close()
        break
      else:
         command_output_response = s.recv(1024).decode('utf-8')
         print(f"Esta fue la salida de tu comando:\n{command_output_response}")
    print('Parece que se cerro la conexion')
    s.close()

# print(f"Recibido del servidor: {data.decode('utf-8')}")
