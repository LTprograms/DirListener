import socket

host = '192.168.1.19'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))

    while True:
        mensaje = input("Ingrese un mensaje (o 'exit' para salir): ")
        
        if mensaje.lower() == 'exit':
            break

        client.sendall(mensaje.encode('utf-8'))

print("Cliente desconectado.")
