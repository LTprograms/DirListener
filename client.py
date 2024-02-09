import socket
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class MyHandler(FileSystemEventHandler):
    __body_dir = ""
    __body_file = ""
    def on_created(self, event):
        if event.is_directory:
            msg = f"{self.__body_dir} {event.src_path} - {datetime.now().strftime('%d/%m/%Y | %H:%M:%S')}"
        else:
            msg = f"{self.__body_file} {event.src_path} - {datetime.now().strftime('%d/%m/%Y | %H:%M:%S')}"

        client.sendall(msg.encode('utf-8'))

    def set_body_dir(self, body):
        self.__body_dir = body

    def set_body_file(self, body):
        self.__body_file = body

host = '192.168.1.19'
# host = '192.168.1.1'
port = 12345
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))

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

            event_handler.set_body_file(data["message"]["body"]["file"])
            event_handler.set_body_dir(data["message"]["body"]["dir"])

            observer.schedule(event_handler, path=directory, recursive=True)
            observer.start()

            try:
                while True:
                    pass
            except KeyboardInterrupt:
                observer.stop()

    except KeyboardInterrupt:
        pass

