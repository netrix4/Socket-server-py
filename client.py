import socket
HOST = '192.168.0.190'
PORT = 555

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Conectado al servidor en {HOST}:{PORT}")
    message = 'Hola, servidor de eco'
    s.sendall(message.encode('utf-8'))
    print(f"Enviado: {message}")
    data = s.recv(1824)

print(f"Recibido del servidor: {data.decode('utf-8')}")
