import socket
from datetime import datetime
import threading


chatrooms = {}
nicks = {}
def handle_client(client, addr):
    room = client.recv(1024).decode("utf-8").strip()
    nickname = client.recv(1024).decode("utf-8")
    print(f"[NOWE POŁĄCZENIE] {addr} , [{room}] ,{nickname}")
    nicks[addr] = nickname
    if room not in chatrooms:
        chatrooms[room] = []
    chatrooms[room].append((client,nickname))
    users_in_room = [nick for _, nick in chatrooms[room]]
    client.send(f"[*] In the room are: {', '.join(users_in_room)}".encode("utf-8"))
    for c, n in chatrooms[room]:
        if c != client:
            c.send(f"[*] {nickname} just joined to the {room}".encode("utf-8"))
    try:
        while True:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = client.recv(1024).decode("utf-8").strip()
            if not msg:
                break
            if msg == "/who":
                client.send(f"[*] In the room are: {', '.join(users_in_room)}".encode("utf-8"))
                continue
            print(f" {time} [{room}] {addr} {nicks[addr]}: {msg}")

            for c,n in chatrooms[room]:
                if c != client:
                    c.send(f"{nicks[addr]}: {msg}".encode("utf-8"))
            if msg == "quit":
                break

    except:
        pass
    finally:
        chatrooms[room] = [(c,n) for c,n in chatrooms[room] if c != client]
        client.close()
        for c,n in chatrooms[room]:
            if c != client:
                c.send(f"[*] {nickname} has disconnected".encode("utf-8"))
        print(f"[ROZŁĄCZONO] {addr} {nicks[addr]}")

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

