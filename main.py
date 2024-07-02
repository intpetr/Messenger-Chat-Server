import socket
import sys
import threading
from threading import Thread
from time import sleep
import pip



import Pairing
from SocketServer import SocketServer



if __name__ == '__main__':

    #maybe databaseconnector should be here in case socketserver crashes
    websocketserver = SocketServer()
    websocketserver.run()





