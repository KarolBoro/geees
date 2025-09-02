import socket
from datetime import datetime
import threading


chatrooms = {}

def handle_client(client, addr):
    print(f"[NOWE POŁĄCZENIE] {addr}")

    room = client.recv(1024).decode("utf-8").strip()
    if room not in chatrooms:
        chatrooms[room] = []
    chatrooms[room].append(client)

    try:
        while True:
            msg = client.recv(1024).decode("utf-8").strip()
            if not msg:
                break
            print(f"[{room}] {addr}: {msg}")

            for c in chatrooms[room]:
                if c != client:
                    c.send(f"Nowy użytkownik dołączył do {room}".encode("utf-8"))
                    c.send(f"{addr}: {msg}".encode("utf-8"))

            if msg == "quit":
                break
    except:
        pass
    finally:
        chatrooms[room].remove(client)
        client.close()
        print(f"[ROZŁĄCZONO] {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5050))
    server.listen()
    print("[SERWER DZIAŁA] Czeka na połączenia...")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

start_server()




# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server.bind(("localhost", 5050))
#
# server.listen()
#
# client, addr = server.accept()
# nazwa_uzytkownika = client.recv(1024).decode('utf-8')
# print(f"Nowy uzytkownik polaczony: {nazwa_uzytkownika}")
#
# done = False
#
# with open("logs.txt", "a") as f:
#     f.write("\n")
#
# while not done:
#     time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     msg = client.recv(1024).decode('utf-8')
#     with open("logs.txt", "a") as f:
#         f.write(time + " | " + nazwa_uzytkownika + " | " + msg + "\n")
#
#     if msg.strip() == "quit":
#         print("Koniec wymiany wiadomości.")
#         break
#     else:
#         print(f"{nazwa_uzytkownika}: {msg}")
#     client.send(f"Server: {input('Twoja odpowiedz: ')}".encode('utf-8'))
#
# client.close()
# server.close()

# dodac nicki do logow, i zebasdasy tez zeby zapisywal to co odbieramy od uzytkownika safasdfasdf
