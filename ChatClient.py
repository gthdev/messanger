import socket as Socket
import _thread

print("A chat program coded in ~~Monty~~ Python!")
# transistion from Java to Python be like:
true = True
false = False

port = 42069

srvaddr = input("input the server's address: ")
nick = ""
while len(nick) < 3 or len(nick) > 20:
    nick = input("enter your nickname (3-20 characters): ").strip()

io = Socket.socket()
print("attempting a connection to /" + srvaddr + ":" + str(port))
try:
    io.connect((srvaddr, port))
    io.send(nick.encode("utf-8"))
    ans = io.recv(32).decode("utf-8")
    print("connected. server's welcome message: '" + ans + "'.")
except Exception:
    print("couldn't connect. check server's address, network status or firewall configuration.")
    exit(-1)

#print("dbg: message receiver thread")
def rx():
    while true:
        print(io.recv(256).decode("utf-8"))

_thread.start_new_thread(rx, (()))

#print("dbg: message sender thread")
while True:
        io.send(input().encode("utf-8"))
io.close()
input("disconnected.")
exit(0)