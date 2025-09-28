import socket
import os
import json
from DTOs.UserAuthResponse import UserAuthResponse

# HOST = '192.168.0.190'
# HOST = '0.0.0.0'
HOST = '192.168.100.79'
PORT = 555

fixed_users=[{'username':'badass420'},{'username':'mario123'}]
isallowedconnection = True

def get_is_valid_user(user_input)->bool:
    for index, fixed_user, in enumerate(fixed_users):
     if user_input == fixed_user['username']:
       return UserAuthResponse(status=200, message="Ok", user_id=index)
    return UserAuthResponse(status=500, message="User not found", user_id=0)

# while True:
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        entered_username = conn.recv(1024).decode('utf-8')

        user_validation_response = get_is_valid_user(entered_username)

        if user_validation_response.status == 200:
            print(f'Bienvenido, {entered_username}')
            print(f"Conectado por {addr}")

            conn.sendall(json.dumps(user_validation_response.to_dict()).encode('utf-8'))

            print('Escuchando clientes...')

            while isallowedconnection:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    print('Creo que aqui se cierra cuando el host se desconecta')
                    conn.close()
                    break
                else:
                    # data = conn.recv(1024).decode('utf-8')
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
                                conn.sendall(output.encode('utf-8'))
                            else:
                                conn.sendall(b"-- Comando sin salida --")
                        except Exception as e:
                            conn.sendall(f"Error: {e}".encode('utf-8'))

        else:
            # ToDo: Ask for create new user
            user_validation_response = json.dumps(user_validation_response.to_dict())
            print('Parece que tu usuario no existe', user_validation_response)
            conn.sendall(user_validation_response.encode('utf-8'))

        conn.close()
    conn.close()
    # break
