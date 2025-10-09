import socket
import json

CHARFORMAT = 'utf-8'
HOST = '192.168.0.190'
PORT = 555

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Conectado al servidor {HOST}:{PORT}")
    return client_socket

def send_credentials(client_socket, username, password):
    credentials = json.dumps({"username": username, "password": password})
    client_socket.sendall(credentials.encode(CHARFORMAT))
    response = client_socket.recv(1024).decode(CHARFORMAT)
    try:
        auth = json.loads(response)
        return auth.get("status") == 200
    except:
        return False

def interactive_shell(client_socket):
    print("Escribe 'quit' para salir.\n")
    while True:
        command = input("Comando > ").strip()
        if not command:
            continue
        client_socket.sendall(command.encode(CHARFORMAT))
        if command == "quit":
            print("bye j0t0")
            break
        output = client_socket.recv(4096).decode(CHARFORMAT)
        print(f" Respuesta:\n{output}")

    client_socket.close()

def main():
    client = connect_to_server()
    username = input("Usuario: ")
    password = input("Contraseña: ")

    if send_credentials(client, username, password):
        print("Entraste, bien canijo")
        interactive_shell(client)
    else:
        print("contrasena mal, vuelvelee a intentar")
        client.close()

if __name__ == "__main__":
    main()
