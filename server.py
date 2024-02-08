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
                # EMAIL INFO
                message = MIMEMultipart()
                message["From"] = data_send["message"]["from"]
                message["To"] = data_send["message"]["to"]
                message["Subject"] = f"Cambios en {data_send['directory']}"

                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                smtp_username = data_send["transmitter"]
                smtp_password = data_send["password"]
                receiver = data_send["receiver"]
                
                message.attach(MIMEText(data.decode('utf-8'), "plain"))
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    # SEND EMAIL
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    server.sendmail(smtp_username, receiver, message.as_string())
