import socket

host = '0.0.0.0'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

    servidor.bind((host, port))
    servidor.listen()

    while True:
        conexion, direccion_cliente = servidor.accept()
        with conexion:
            print(f"Conexión establecida desde {direccion_cliente}")

            datos = conexion.recv(1024)
            if not datos:
                break

            print(f"Datos recibidos: {datos.decode('utf-8')}")
