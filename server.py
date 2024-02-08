import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

host = '0.0.0.0'
port = 12345



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    server.bind((host, port))
    server.listen()

    print(f"Esperando conexiones en {host}:{port}")
    while True:
        connection, client = server.accept()
        print(f"Conexión establecida desde {client}")
        with connection:
            while True:
                with open('data.json', 'r') as file:
                    data_json = file.read()

                data_send = json.loads(data_json)
                connection.sendall(json.dumps(data_send).encode('utf-8'))

                data = connection.recv(1024)
                if not data:
                    break 
                print(f"Datos recibidos: {data.decode('utf-8')}")
