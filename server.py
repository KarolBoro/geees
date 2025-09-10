import socket
from datetime import datetime
import threading
import mysql.connector
import emoji

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "geees"
)

mycursor = mydb.cursor()

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
    client.send(f"[*] In the '{room}' room are: {', '.join(users_in_room)}".encode("utf-8"))
    for c, n in chatrooms[room]:
        if c != client:
            c.send(f"[*] {nickname} just joined to the {room}".encode("utf-8"))
    try:
        while True:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = client.recv(1024).decode("utf-8").strip()
            msg = emoji.emojize(msg)
            if not msg:
                break

            if msg.startswith("/create"):
                parts_new_room = msg.split(" ", 1)
                if len(parts_new_room) < 2:
                    client.send(f"[*] To create new room use: /create <ROOM_NAME> ".encode("utf-8"))
                    continue

                new_room = parts_new_room[1]

                if new_room in chatrooms:
                    client.send(f"[*] Room '{new_room}' already exists!".encode("utf-8"))
                    continue

                chatrooms[room] = [(c, n) for c, n in chatrooms[room] if c != client]
                for c, n in chatrooms[room]:
                    c.send(f"[*] {nickname} has left the room.".encode("utf-8"))

                if not chatrooms[room]:
                    del chatrooms[room]

                room = new_room
                chatrooms[room] = [(client, nickname)]
                client.send(f"[*] You created and joined room '{room}'".encode("utf-8"))

            if msg.startswith("/join"):
                parts_join = msg.split(" ",1)
                if len(parts_join) < 2:
                    client.send(f"[*] To join to other room please type: /join <NAME_OF_OTHER_ROOM>".encode("utf-8"))
                    continue
                other_room = parts_join[1]

                if other_room not in chatrooms:
                    client.send(f"[*] Room of this name doesnt exist!".encode("utf-8"))
                    continue

                chatrooms[room] = [(c, n) for c, n in chatrooms[room] if c != client]
                for c, n in chatrooms[room]:
                    c.send(f"[*] {nickname} has left the room.".encode("utf-8"))

                if not chatrooms[room]:
                    del chatrooms[room]

                room = other_room
                chatrooms[room].append((client,nickname))
                client.send(f"[*] You have joined to channel '{other_room}'!".encode("utf-8"))
                for c,n in chatrooms[room]:
                    if c != client:
                        c.send(f"[*] {nickname} has joined the room".encode("utf-8"))
                continue

            if msg == "/who":
                users_in_room = [nick for _, nick in chatrooms[room]]
                client.send(f"[*] In the '{room}' room are: {', '.join(users_in_room)}".encode("utf-8"))
                continue

            if msg in ["/commands", "/?", "/command"]:
                client.send(f"[*] Hello! Available commands are:\n"
                            f"/who - list of users in channel\n"
                            f"/rooms - list of available channels\n"
                            f"/create <room_name> - create your own channel\n"
                            f"/join <name_of_channel> - join to another available channel\n"
                            f"/nick <new_name> - change your nickname\n"
                            f"/emojis - list of available emoji's\n"
                            f"/quit - leave the chat".encode("utf-8"))
                continue
            if msg == "/rooms":
                rooms_list = ', '.join(chatrooms.keys())
                client.send(f"[*] Active rooms: {rooms_list}".encode("utf-8"))
                continue

            if msg == "/emojis":
                client.send(f"Available emoji's : https://carpedm20.github.io/emoji/".encode("utf-8"))
                continue

            if msg.startswith("/nick"):
                parts_new_nickname = msg.split(" ",1)
                if len(parts_new_nickname) < 2:
                    client.send(f"[*] To change nickname use: /nick <NEW_NICKNAME>".encode("utf-8"))
                    continue

                new_nickname = parts_new_nickname[1]
                old_nickname = nickname
                nickname = new_nickname
                nicks[addr] = new_nickname
                chatrooms[room] = [(c, new_nickname if c == client else n) for c, n in chatrooms[room]]
                users_in_room = [nick for _, nick in chatrooms[room]]
                client.send(f"[*] Your NICKNAME has been changed to {new_nickname}".encode("utf-8"))
                for c, n in chatrooms[room]:
                    if c != client:
                        c.send(f"[*] From now {old_nickname} is known as {new_nickname}".encode("utf-8"))
                        print(f"[*] From now {old_nickname} is known as {new_nickname}")
                continue

            print(f" {time} [{room}] {addr} {nicks[addr]}: {msg}")

            sql = "INSERT into logs(Date_time, Room, Nickname, MSG) VALUES (%s, %s, %s, %s)"
            val = (time,room,nickname,msg)
            mycursor.execute(sql,val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")

            for c,n in chatrooms[room]:
                if c != client:
                    c.send(f"[{time}] {nickname}: {msg}".encode("utf-8"))
            if msg.strip() == "/quit":
                break

    except:
        pass
    finally:
        user_nick = nicks.get(addr, nickname)
        chatrooms[room] = [(c,n) for c,n in chatrooms[room] if c != client]
        client.close()

        for c,n in chatrooms[room]:
            if c != client:
                c.send(f"[*] {user_nick} has disconnected".encode("utf-8"))

        print(f"[ROZŁĄCZONO] {addr} {user_nick}")

        if addr in nicks:
            del nicks[addr]

        if not chatrooms[room]:
            print(f"[POKOJ NR [{room}] ZOSTAL USUNIETY]")
            del chatrooms[room]


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

mydb.close()
