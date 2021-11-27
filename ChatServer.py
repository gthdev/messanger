import socket as Socket
import _thread
import os, time, datetime

# Java developer in Python be like:
true = True
false = False

ifconfig = "0.0.0.0"
port = 42069
clients = []

try:
    if not os.path.exists("logs"):
        os.makedirs("logs")
    path = "logs/log-"+str(datetime.datetime.now()).replace(" ", "_") + ".txt"
    print(path)
    logFile = open(str(path), "at")
except IOError as e:
    print("Failed to create a log file: ", e)
    logFile = None
    
def log(text):
    text = text + f"[{time.ctime(time.time())}] "
    print(text)
    try:
        logFile.write(text + "\n")
    except IOError:
        pass

log(f"Starting ChatServer on /{ifconfig}:{port}")

class Klient:
    def __init__(self,  cl):
        self.sck  = cl[0]
        self.addr = cl[1]
        self.nick = self.sck.recv(20).decode("utf-8")
        for client in clients:
            if(client.nick == self.nick and client.addr != self.addr):
                self.sck.close()
        self.sendUTF("Siemanko, witam w mojej kuchni!")
        log("Client connected: " + self.nick + "@" + str(self.addr))
    def format(self):
        return "["+ self.nick + "]: "
    def recv(self):
        return self.sck.recv(256)
    def recvUTF(self):
        return format(self) + self.recv(self).decode("utf-8")
    def send(self, usr):
        return self.sck.send(usr)
    def sendUTF(self, msg):
        print(msg)
        return self.sck.send(msg.encode("utf-8"))

# print("server socket")
skt = Socket.socket()
skt.bind((ifconfig, port))
skt.listen(2)

def broadcast(msg):
    for client in clients:
            try:
                client.send(msg)
            except Exception as e:
                log("error L2: ", e)
                clients.remove(client)

def server_thread(cl):
    while True:
        try:
            msg = cl.recv()
            usr = cl.format()
            log(usr + msg.decode("utf-8"))
            usr = usr.encode("utf-8")
            broadcast(usr + msg)
        except Exception as e:
            log("error L1: " + e)

def server_messaging():
    while true:
        msg = "{ S e r v e r @ " + str(port) + " }: " + input("Enter a message to be send as @server..\r\n")
        broadcast(msg.encode("utf-8"))
_thread.start_new_thread(lambda: server_messaging(), (()))

# print("client listener")
log("The server is awaiting clients.")
while True:
    cl = Klient(skt.accept())
    clients.append(cl)
    thread = _thread.start_new_thread(lambda c: server_thread(c), ((cl, )))