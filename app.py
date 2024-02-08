import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MyHandler(FileSystemEventHandler):
    def __init__(self, message:MIMEMultipart, owner:str, email:str) -> None:
        super().__init__()
        self.__message = message
        # SERVER INFO
        self.__smtp_server = "smtp.gmail.com"
        self.__smtp_port = 587
        self.__smtp_username = owner
        self.__smtp_password = "lmmz ggep nlac epxt"
        self.__email = email

    def on_created(self, event):
        if event.is_directory:
            body = f"Se ha creado un directorio: {event.src_path}"
        else:
            body = f"Se ha creado un archivo: {event.src_path}"
        self.__message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.__smtp_server, self.__smtp_port) as server:
            # SEND EMAIL
            server.starttls()
            server.login(self.__smtp_username, self.__smtp_password)
            server.sendmail(self.__smtp_username, self.__email, self.__message.as_string())
        print(body)


with open('data.json', 'r') as file:
    data_json = file.read()

data = json.loads(data_json)

directory = data["directories"][0]

# EMAIL INFO
message = MIMEMultipart()
message["From"] = "PYTHON"
message["To"] = data["emails"][1]
message["Subject"] = f"Cambios en {directory}"

# WATCHDOG LISTENER
event_handler = MyHandler(message, data["emails"][0], data["emails"][1])
observer = Observer()
observer.schedule(event_handler, path=directory, recursive=True)

print(f"Observando el directorio: {directory}")

observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()