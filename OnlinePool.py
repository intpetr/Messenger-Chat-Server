class message:

    def __init__(self, senderid, receiverid, text):
        self.senderid = senderid
        self.receiverid = receiverid
        self.text = text
        print("New message object created with attributes: "+ str(senderid),str(receiverid),str(text))


class OnlinePool:

    def __init__(self):
        self.onlinemessagelist = []
        self.pool = []

    def isonline(self, id):
        if int(id) in self.pool:
            print("Found online: " + str(id))
            return True
        else:
            print("Found offline: " + str(id))
            return False

    def online(self, id):
        self.pool.append(int(id))
        print(str(id) + " is now online")



    def offline(self, id):
        self.pool.remove(int(id))

    def hasonlinemessage(self, id):
        #print("Online message checking for " + str(id))
        for mess in self.onlinemessagelist:
            print(mess.receiverid,id)
            print(int(mess.receiverid) == int(id))
            if int(mess.receiverid) == int(id):

                print("Online message found for " + str(id))
                return True

        print("No oline message found for " + str(id))
        return False

    def getonlinemessage(self, myid):

        for x in range(0, len(self.onlinemessagelist)):

            if int(self.onlinemessagelist[x].receiverid) == int(myid):
                text = self.onlinemessagelist[x].text
                sender = self.onlinemessagelist[x].senderid

                del self.onlinemessagelist[x]

                return str(sender), str(text)

    def addonlinemessage(self, myid, receiverid, text):
        print("online message added for " + str(receiverid))
        self.onlinemessagelist.append(message(myid, receiverid, text))
