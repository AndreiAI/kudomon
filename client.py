import sys
import time
from utils import Client

class MyClient(Client):
    def onMessage(self, socket, message):
        print message   #print incoming message
        return True

ip = sys.argv[1]    #get IP
port = int(sys.argv[2]) #get PORT
screenName = sys.argv[3]    #get chosen Name

client = MyClient()

client.start(ip, port)

#Echo the name
client.send('REGISTER %s' % screenName) #send the register message

while client.isRunning():
    try:
        message = raw_input('> ').strip()
        client.send(message)
    except:
        client.stop()

client.stop()
