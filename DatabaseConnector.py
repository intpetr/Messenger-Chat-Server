import mysql.connector

import Pairing


class DatabaseConnector:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="-----",
            user="-----",
            password="-----"
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute("USE chat;")


    def auth(self, username, password):
        self.cursor.execute("SELECT * FROM Users WHERE Username='" + username + "' AND Password='" + password + "';")
        myresult = self.cursor.fetchall()
        row = [item[0] for item in myresult]
        if len(row) == 0:
            print("Auth unsuccessful")
            return -1
        else:
            return int(row[0])

    def getlastmessage(self,receiverid,senderid):
        pass
        sql = "SELECT TOP 1 Text FROM PrivateMessages WHERE Chatid='"+str(self.getchatid(receiverid,senderid))+"' AND NOT Senderid='"+receiverid+"';"


    def writemsg(self, senderid, receiverid, text):
        sql = "INSERT INTO PrivateMessages (Chatid,Senderid,Text) VALUES ('"+str(self.getchatid(senderid,receiverid))+"','"+str(senderid)+"','"+text+"');"
        #print(sql)
        self.cursor.execute(sql)
        self.mydb.commit()
        print("Message write executed")



    def createChat(self, firstid, secondid):
        if not (firstid > secondid):
            firstid, secondid = secondid, firstid

        sql = "INSERT INTO PrivateChats 'Chatid,User1id,User2id) VALUES ('"+str(self.getchatid(firstid,secondid))+"','" + firstid + "','" + secondid + "');"
        self.cursor.execute(sql)
        self.mydb.commit()

    def getchatid(self, firstid, secondid):

        return Pairing.pair(int(firstid),int(secondid))

        #Cantor Párosítással helyettesítve
        #if not (firstid > secondid):
        #    firstid, secondid = secondid, firstid
        #sql = "SELECT TOP 1 Chatid FROM PrivateChats WHERE User1id='"+firstid+"' User2id='"+secondid+"';"
        #self.cursor.execute(sql)
        #myresult = self.cursor.fetchall()
        #row = [item[0] for item in myresult]

    # csak akkor fog lefutni amikor addolják egymást
    def HasConversation(self, firstid, secondid):
        sql = "SELECT * FROM PrivateChats WHERE User1id='" + firstid + "' AND User2id='" + secondid + "';"
        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()
        row = [item[0] for item in myresult]
        if len(row) == 0:
            pass
