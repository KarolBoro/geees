import socket
from datetime import  datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 5050))

server.listen()

client, addr = server.accept()
nazwa_uzytkownika = client.recv(1024).decode('utf-8')
print(f"Nowy uzytkownik polaczony: {nazwa_uzytkownika}")

done = False
time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

while not done:
    msg = client.recv(1024).decode('utf-8')
    if msg == "quit":
        done = True
        print("Koniec wymiany wiadomości.")
        with open("logs.txt", "a") as f:
            f.write(time + " " + msg + "\n")
        break

    else:
        print(f"{nazwa_uzytkownika}: {msg}")
    client.send(f"Server: {input('Twoja odpowiedz: ')}".encode('utf-8'))
    with open("logs.txt", "a") as f:
        f.write(time + " " + nazwa_uzytkownika + " " + msg + "\n")

client.close()
server.close()

# dodac nicki do logow, i zebasdasy tez zeby zapisywal to co odbieramy od uzytkownika safasdfasdf
# nnnn