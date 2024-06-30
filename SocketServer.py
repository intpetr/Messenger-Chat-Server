import base64
import socket
import sys
import threading
import time
import gzip
import zlib
import pickle
import random



from threading import Thread
from time import sleep

from DatabaseConnector import DatabaseConnector
from OnlinePool import OnlinePool
from WebsocketAuth import WebsocketAuth


class SocketServer:

    def __init__(self):
        # connector = DatabaseConnector()
        self.db = DatabaseConnector()
        pool = OnlinePool()
        self.online = pool
        self.wsauth = WebsocketAuth()

    def logmessage(self,senderid,receiverid,text):
        self.db.writemsg(senderid,receiverid,text)



    def receiveClientMessage(self, conn):
        #needs cleanup
        header = conn.recv(2)
        FIN = bool(header[0] & 0x80)  # bit 0
        assert FIN == 1, "We only support unfragmented messages"
        opcode = header[0] & 0xf  # bits 4-7
        assert opcode == 1 or opcode == 2, "We only support data messages"
        masked = bool(header[1] & 0x80)  # bit 8
        assert masked, "The client must mask all frames"
        payload_size = header[1] & 0x7f  # bits 9-15
        assert payload_size <= 125, "We only support small messages"
        masking_key = conn.recv(4)
        payload = bytearray(conn.recv(payload_size))
        for i in range(payload_size):
            payload[i] = payload[i] ^ masking_key[i % 4]
        return payload.decode('utf-8')


    def NewThread(self, conn):

        print("New client thread started")


        #working



        # splitted here ONLY splitted = login.split(" ")
        #working

        login = conn.recv(1024).decode('ascii')
        print(login)
        print('Creating response')

        conn.sendall(str(self.wsauth.get_response(login)).encode('ascii'))
        print(str(self.wsauth.get_response(login)))




        print("Websocket handshake successful")
        #conn.sendall("hello".encode('utf-8'))


        message = self.receiveClientMessage(conn)
        print(message)


        conn.send("pong".encode())


        #print(str(bytes, encoding="utf8"))


        #print(gzip.decompress(response))
        #bytes = zlib.decompress(response)


        time.sleep(100)
        conn.sendall("hello".encode('ascii'))


        time.sleep(30)
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
        self.HOST = '0.0.0.0'
        self.PORT = 9999

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
            #Egy probank jo lenne kiprobalni hgoy ha itt hasznalom a connection.bind() ot más portra akkor azon lesz-e a kapcsolat. Ha igen akkor meggyozodni rola hogy
            #az a port meg van-e nyitva a routeren.
            thread = threading.Thread(target=self.NewThread, args=(connection,))
            thread.start()

            print("A new client connected")
            print("Active threads " + str(threading.active_count()))
        s.close()


