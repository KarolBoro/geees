import socket
from datetime import datetime
import threading

def listen_for_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if msg:
                print(msg)
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5050))

nickname = input("Podaj nazwe uzytkownika: ")
room = input("Do którego pokoju chcesz wejść? ")
client.send(room.encode("utf-8"))
client.send(nickname.encode("utf-8"))
# wątek nasłuchujący
thread = threading.Thread(target=listen_for_messages, args=(client,))
thread.start()

while True:
    wiadomosc = input()
    client.send(wiadomosc.encode("utf-8"))
    if wiadomosc.strip() == "quit":
        break

client.close()
