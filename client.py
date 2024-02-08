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

    @property
    def message(self):
        return self.__msg
    
    def set_msg(self, msg):
        self.__msg = msg


host = '192.168.1.19'
port = 12345

# WATCHDOG LISTENER


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))
    try:
        while True:

            data_server = client.recv(1024)
            if not data_server:
                break

            data = json.loads(data_server.decode('utf-8'))
            directory = data["directory"]

            event_handler = MyHandler()
            observer = Observer()
            # observer.schedule(event_handler, path=directory, recursive=True)

            observer.start()
            
            observer.schedule(event_handler, path=directory, recursive=True)

            client.sendall(event_handler.message.encode('utf-8'))
            print(f"Enviado: {event_handler.message}")
            event_handler.set_msg("")
            
    except KeyboardInterrupt:
        observer.stop()
print("Cliente desconectado.")
