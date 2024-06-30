import base64
import hashlib


class WebsocketAuth:

    def __init__(self):
        self.init = True

    def convert_string_to_hash(self, word):
        digest = hashlib.sha1(word.encode('utf-16-le')).digest()
        return base64.b64encode(digest)

    def stackoverflowsolution(self,key):
        pass
        shalf = hashlib.sha1()
        shalf.update

    def get_Accept_key(self, fullmessage):

        splitted = fullmessage.split(" ")
        index = -1

        for i in range(0, len(splitted)):

            #print("=" in splitted[i], splitted[i])
            if "=" in splitted[i]:
                print("The whole section is: "+repr(splitted[i]))

                keyandcode = splitted[i] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                key = splitted[i]
                splitter = '\\r\\'
                print(splitter)
                sankey = splitted[i].split(splitter)
                key = key[:-24]
                print("THE KEY IS: "+repr(key))
                #key = "dGhlIHNhbXBsZSBub25jZQ=="
                #sha1hash = hashlib.sha1(keyandcode.encode()).digest()  # or .digest() instead of hexdigest()
                #print("LOGIN INGO LOGIN INFO HERE HALO" + str(sha1hash))

                shalf = hashlib.sha1()
                shalf.update(key.encode('utf-8') + guid.encode('utf-8'))
                return base64.b64encode(shalf.digest()).decode('utf-8')

                #return self.convert_string_to_hash(keyandcode)

                #shalf = hashlib.sha1()
                #shalf.update(key.encode('utf-8') + guid.encode('utf-8'))
                #return base64.b64encode(shalf.digest()).decode('utf-8')  ez a három sor helyes talan

                #return sha1hash

        return "bad text processing"

    def get_response(self, fullmessage):
        print("Response creator method called")
        # rawstring template indicated by r in beginnning

        rt = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n" + "Connection: Upgrade\r\n" + "Sec-WebSocket-Accept: insertkeyhere\r\n\r\n"
        responseTemplate = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: insertkeyhere\r\n\r\n"
        response = rt.replace('insertkeyhere', self.get_Accept_key(fullmessage))
        #base64.b64encode(sha1hash)
        return response

    # close but wrong results: response = rt.replace('insertkeyhere', str(base64.b64encode(self.get_Accept_key(fullmessage)).decode("utf-8")))
    # response = rt.replace('insertkeyhere', str(base64.b64encode(self.get_Accept_key(fullmessage)).decode("utf-8")))

#probable solution:
#https://stackoverflow.com/questions/35733989/python-web-socket-handshake-not-working