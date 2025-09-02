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

room = input("Do którego pokoju chcesz wejść? ")
client.send(room.encode("utf-8"))

# wątek nasłuchujący
thread = threading.Thread(target=listen_for_messages, args=(client,))
thread.start()

while True:
    wiadomosc = input()
    client.send(wiadomosc.encode("utf-8"))
    if wiadomosc.strip() == "quit":
        break

client.close()








# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#
# try:
#     client.connect(("localhost", 5050))
# except:
#     print("Przypal z serwerem :<")
#
# done = False
# nazwa_uzytkownika = input("Podaj nazwe uzytkownika: ")
# client.send(nazwa_uzytkownika.encode('utf-8'))
# while not done:
#     time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     client.send(input("Wiadomosc: ").encode('utf-8'))
#     msg = client.recv(1024).decode('utf-8')
#     with open("logs.txt", "a") as f:
#         f.write(time + " | " + msg + "\n")
#     if msg.strip() == "quit":
#         print("Koniec wymiany wiadomości.")
#         break
#     else:
#         print(msg)
#
# client.close()
