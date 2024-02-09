import socket
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            msg = f"Se ha creado un directorio: {event.src_path}"
        else:
            msg = f"Se ha creado un archivo: {event.src_path}"

        # Enviar el mensaje al servidor cuando se crea un archivo
        client.sendall(msg.encode('utf-8'))
        print(f"Enviado: {msg}")

# Configuración del cliente
host = '192.168.1.19'
# host = '192.168.1.1'
port = 12345
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))

        # Crear el observador y el manejador de eventos
        event_handler = MyHandler()
        observer = Observer()

        try:
            while True:
                data_server = client.recv(1024)
                if not data_server:
                    break

                data = json.loads(data_server.decode('utf-8'))
                directory = data["directory"]

                # Configurar el observador y el manejador de eventos
                observer.schedule(event_handler, path=directory, recursive=True)
                observer.start()

                try:
                    while True:
                        pass
                except KeyboardInterrupt:
                    observer.stop()

        except KeyboardInterrupt:
            pass

    print("Cliente desconectado.")
except:
    exit()