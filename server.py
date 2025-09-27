import socket
# HOST = '192.168.0.190'
# HOST = '0.0.0.0'
HOST = '192.168.100.79'
PORT = 555

fixed_users=[{'username':'badass420'},{'username':'mario123'}]
isallowedconnection = True

def get_is_valid_user(user_input)->bool:
    for fixed_user in fixed_users:
     if user_input == fixed_user['username']:
       return True
    return False

# while True:
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        entered_username = conn.recv(1024)
        print(entered_username.decode('utf-8'))

        if get_is_valid_user(entered_username.decode('utf-8')):
            print('Asi es, si existe')
            print(f"Conectado por {addr}")
            conn.sendall('si'.encode('utf-8'))

            while isallowedconnection:
                print('Escuchando clientes...')
                data = conn.recv(1024)
                print(f"Recibido: {data.decode('utf-8')}")
                if data.decode('utf-8') == 'quit':
                    print('Cerrando conexion')
                    # conn.sendall('Cerrando conexion'.encode('utf-8'))
                    conn.close()
                    isallowedconnection = not isallowedconnection
                if not data:
                    print('Creo que aqui se cierra cuando el host se desconecta')
                    conn.close()
                    break

        else:
            print('Parece que tu usuario no existe')
        #    conn.sendall('Parece que tu usuario no existe'.encode('utf-8'))

        conn.close()
    conn.close()
