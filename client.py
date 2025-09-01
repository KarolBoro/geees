import socket
from datetime import datetime

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    client.connect(("localhost", 5050))
except:
    print("Przypal z serwerem :<")

done = False
nazwa_uzytkownika = input("Podaj nazwe uzytkownika: ")
client.send(nazwa_uzytkownika.encode('utf-8'))
while not done:
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client.send(input("Wiadomosc: ").encode('utf-8'))
    msg = client.recv(1024).decode('utf-8')
    with open("logs.txt", "a") as f:
        f.write(time + " | " + msg + "\n")
    if msg.strip() == "quit":
        print("Koniec wymiany wiadomości.")
        break
    else:
        print(msg)

client.close()
