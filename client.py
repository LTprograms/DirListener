import socket
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    __msg = ""

    def on_created(self, event):
        if event.is_directory:
            msg = f"Se ha creado un directorio: {event.src_path}"
        else:
            msg = f"Se ha creado un archivo: {event.src_path}"
        
        self.__msg = msg
        print(self.__msg)

    @property
    def message(self):
        return self.__msg
    
    def set_msg(self, msg):
        self.__msg = msg

# Configuración del cliente
host = '192.168.1.19'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))

    # Crear el observador y el manejador de eventos fuera del bucle
    event_handler = MyHandler()
    observer = Observer()

    try:
        while True:
            data_server = client.recv(1024)
            print(data_server)
            if not data_server:
                break

            data = json.loads(data_server.decode('utf-8'))
            directory = data["directory"]

            # Configurar el observador y el manejador de eventos
            observer.schedule(event_handler, path=directory, recursive=True)
            observer.start()

            # Esperar hasta que se reciba un mensaje del manejador de eventos
            observer.join()

            # Enviar el mensaje al servidor
            client.sendall(event_handler.message.encode('utf-8'))
            print(f"Enviado: {event_handler.message}")

            # Limpiar el mensaje después de enviarlo
            event_handler.set_msg("")

    except KeyboardInterrupt:
        observer.stop()

print("Cliente desconectado.")
