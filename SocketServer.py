import socket
import sys
import threading
import time



from threading import Thread
from time import sleep

from DatabaseConnector import DatabaseConnector
from OnlinePool import OnlinePool


class SocketServer:

    def __init__(self):
        # connector = DatabaseConnector()
        self.db = DatabaseConnector()
        pool = OnlinePool()
        self.online = pool

    def logmessage(self,senderid,receiverid,text):
        self.db.writemsg(senderid,receiverid,text)


    def NewThread(self, conn):

        print("New client thread started")

        login = conn.recv(1024).decode('ascii')
        splitted = login.split(" ")

        username = splitted[0]
        password = splitted[1]
        id = self.db.auth(username, password)

        if id > 0:
            conn.sendall("szep volt".encode('ascii'))
            self.online.online(id)

        else:
            conn.sendall("Auth failed".encode('ascii'))
            conn.close()
            print("Connection terminated, killing thread")
            sys.exit()

        time.sleep(2)

        while True:

            #megnézem hgoy kell e kuldeni neki vissza valamit

            if self.online.hasonlinemessage(id):

                messageobj = self.online.getonlinemessage(id)
                #Új protokolt kell kitalálni üzenet fogadásra
                objtext = messageobj[0]+" "+messageobj[1]
                conn.sendall(objtext.encode('ascii'))

            #elkükdöm az üzenetét

            else:
                conn.sendall("0".encode('ascii'))
                #0 : mint a 0 exit code -> Minden  oké, nincs üzenete

            #ha semmit nem kell neki küldenem akkor küldök egy üres üzenetetd



            msg = conn.recv(1024).decode('ascii')
            splitmsg = msg.split(" ")

            if msg == "":
                self.online.offline(id)
                break
            elif msg[0] == "p":
                pass
                #user is present
            elif msg[0] == "t":
                pass
                #user is typing
            elif msg[0] == "m":

                receiverid = splitmsg[1]
                text = msg.split("m "+receiverid+" ")[1]
                print("Senderid "+str(id))
                print("Receiverid "+str(receiverid))
                print("Text "+text)
                self.logmessage(id,receiverid,text)

                if self.online.isonline(receiverid):
                    self.online.addonlinemessage(id,receiverid,text)


            #user wants to send a message



            #print(msg)
            print("Active threads " + str(threading.active_count()))
            # conn.sendall("reply".encode('ascii'))

        conn.close()
        #self.online.offline(id)
        print("connection ended")



    def run(self):
        self.HOST = 'localhost'
        self.PORT = 65000

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except OSError as msg:
            print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg)
            sys.exit(0)

        print("[-] Socket Created")

        # bind socket
        try:
            self.s.bind((self.HOST, self.PORT))
            print("[-] Socket Bound to port " + str(self.PORT))
        except socket.error as msg:
            print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
            sys.exit()

        self.s.listen(10)
        print("LIstening for connections...")
        print("Active threads " + str(threading.active_count()))

        while True:
            # blocking call, waits to accept a connection
            connection, addr = self.s.accept()
            print("[-] Connected to " + addr[0] + ":" + str(addr[1]))
            if connection is None:
                print("Connectin is NULL")

            thread = threading.Thread(target=self.NewThread, args=(connection,))
            thread.start()

            print("A new client connected")
            print("Active threads " + str(threading.active_count()))
        s.close()


