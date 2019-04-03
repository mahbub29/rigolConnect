#!/usr/bin/env python
#-*- coding:utf-8 –*-
#—————————————————————————–
# The short script is a example that open a socket, sends a query,
# print the return message and closes the socket.
#—————————————————————————–
import socket # for sockets
import select
import sys # for exit
import time # for sleep
#—————————————————————————–
remote_ip = "169.254.1.5" #Siglent = "10.0.0.69" #"192.168.0.17" # should match the instrument's IP address
port = 5555 #5024 # the port number of the instrument service
count = 0

#####   P  Y  T  H  O  N      3  .  6      V  E  R  S  I  O  N   #####

def SocketConnect():
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()
    try:
        #Connect to remote server
        s.connect((remote_ip , port))
        r, _, _ = select.select([s], [], [],0.5)
        if r:
            info = s.recv(4096)
            print(info)
    except socket.error:
        print('failed to connect to ip ' + remote_ip)
        print(socket.error)
    return s

def SocketQuery(Sock, cmd):
    reply = None
    try :
        #Send cmd string
        Sock.sendall(cmd)
        print(time.time())
        time.sleep(1)
    except socket.error:
        #Send failed
        print('Send failed')
        sys.exit()
    r, _, _ = select.select([Sock], [], [],0.5)
    if r:
       reply = Sock.recv(4096)
    return reply

def SocketClose(Sock):
    #close the socket
    Sock.shutdown(1)
    time.sleep(5)
    Sock.close()
    time.sleep(.300)

def main():
    global remote_ip
    global port
    global count

# Body: send the SCPI commands *IDN? 10 times and print the return message
try :
    so = SocketConnect()
    SocketQuery(so,b'*IDN?\n')
    while 1:
        LAN_SCPI_Code = (input("Please Enter SCPI command for RIGOL DP832A:\n"))
        LAN_SCPI_Code = bytes(LAN_SCPI_Code+"\n","utf-8")
        LAN_qStr = SocketQuery(so, LAN_SCPI_Code)
        print(time.time())
        print("RIG Says: " + str(LAN_qStr))

    SocketClose(so)
except KeyboardInterrupt:
    print("Program Interrupted and Closed")
    sys.exit()

if __name__ == '__main__':
    proc = main()
