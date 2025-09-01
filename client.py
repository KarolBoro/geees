import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("localhost", 5050))
except:
    print("Przypal z serwerem :<")

done = False
nazwa_uzytkownika = input("Podaj nazwe uzytkownika: ")
client.send(nazwa_uzytkownika.encode('utf-8'))
while not done:
    client.send(input("Wiadomosc: ").encode('utf-8'))
    msg = client.recv(1024).decode('utf-8')
    if msg == "quit":
        done = True
        print("Koniec wymiany wiadomości.")
        break
    else:
        print(msg)

client.close()
