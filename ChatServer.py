import socket as Socket
import _thread
import os, time, datetime

# Java developer starting coding in Python be like:
true = True
false = False

ifconfig = "0.0.0.0"
port = 42069
clients = []

try:
    if not os.path.exists("logs"):
        os.makedirs("logs")
    file = "log-"+str(datetime.datetime.now()).replace(" ", "_").replace(":", ".") + ".txt"
    logFile = open(os.path.join(os.getcwd(), "logs", file), "w+")
except IOError as e:
    print("Failed to create a log file: ", e)
    logFile = None

def log(text):
    text = f"[{time.ctime(time.time())}] " + text
    print(text)
    try:
        logFile.write(text + "\n")
        logFile.flush()
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
        log(msg)
        return self.sck.send(msg.encode("utf-8"))
    def getNickname(self):
        return self.nick
    def getAddr(self):
        return self.addr
    

# print("server socket")
skt = Socket.socket()
skt.bind((ifconfig, port))
skt.listen(2)

def broadcast(msg):
    log(msg.decode("utf-8"))
    for client in clients:
            try:
                client.send(msg)
            except Exception as e:
                log(f"[{client.getNickname()}@{client.getAddr()}] error L2: " + str(e))
                clients.remove(client)

def server_thread(cl):
    while True:
        try:
            msg = cl.recv()
            usr = cl.format().encode("utf-8")
            broadcast(usr + msg)
        except Exception as e:
            log(f"[{cl.getNickname()}@{cl.getAddr()}] error L1: " + str(e))
            break

def server_messaging():
    while true:
        inp = input("Enter a message to be send as @server..\r\n")
        if inp.startswith("/"):
            if(inp[1:].startswith("stop")):
                broadcast("Server shutting down!")
                exit(0)
        else:
            msg = "{ S e r v e r @ " + str(port) + " }: " + inp
            broadcast(msg.encode("utf-8"))
_thread.start_new_thread(lambda: server_messaging(), (()))

# print("client listener")
log("The server is awaiting clients.")
while True:
    cl = Klient(skt.accept())
    clients.append(cl)
    thread = _thread.start_new_thread(lambda c: server_thread(c), ((cl, )))