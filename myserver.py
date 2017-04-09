import sys
from utils import Server
import random
from random import randint

class Kudomon():
    def __init__(self, name, typee, x, y):
        self.name = name    #Kudomon name
        self.type = typee   #Type, eg water / fire etc
        self.x = x          #Position X
        self.y = y          #Position Y
        self.hp = randint(50, 200)  #Hitpoints between 50 and 200
        self.cp = randint(5, 30)    #Combat points between 5 and 30
        self.owner = ''             #Owner, default none
        self.bonus = {}             #There could have been a better way of doing it, but quick hack
        self.bonus['water,fire'] = 1.5
        self.bonus['fire,grass']= 1.5
        self.bonus['grass,rock']= 1.5
        self.bonus['rock,electric']= 1.5
        self.bonus['electric,water']= 1.5
        self.bonus['psihic,water']= 1.5
        self.bonus['psihic,fire']= 1.5
        self.bonus['psihic,grass']= 1.5
        self.bonus['psihic,rock']= 1.5
        self.bonus['psihic,electric']= 1.5

    def move(self):
        '''Wanted to make the kudomons move from time to time, would have been a pain for catching them via terminal'''
        while True:
            self.x += randint(-1, 1)
            self.y += randint(-1, 1)
            if 0 <= self.x and self.x <= 100 and 0 <= self.y and self.y <= 100:
                break

    def fight(self, enemy):
        '''This Kudomon fights enemy Kudomon'''
        bonuss = 1.0    #bonus if not effective against the other type
        #bonus if effective against the other type
        if str(self.type + ',' + enemy.type) in self.bonus:
            bonuss = self.bonus[str(self.type + ',' + enemy.type)]
        #mess is the message that will be returned at the end of the fight
        mess = self.display() + ' attacks ' + enemy.display() + 'inflicting '
        #damage formula:
        damage = int(self.cp * randint(7, 12) / 10 * bonuss)
        enemy.hp -= damage  #self explanatory
        mess += str(damage) + ' damage.'
        if damage > self.cp:
            mess += ' It is SUPER EFFECTIVE!\t' #good old days
        else:
            mess += ' \t'
        mess += enemy.display()
        return mess

    def display(self):
        '''Return info about the Kudomon'''
        return (str(self.name) + ': ' + str(self.type) + '(' + str(self.hp) + ', ' + str(self.cp) + ')')

class Player():
    '''Trainer'''
    def __init__(self, socket, name):
        self.socket = socket    #socket used, needed in identification
        self.name = name    #Chosen name
        self.x = randint(0, 100)    #Position X
        self.y = randint(0, 100)    #Position Y
        self.kudomons = []  #List of kudomons available (in kudoballs)
        self.score = 0  #Score
        self.challenged = False #If he has been challenged by another player
        self.challengedBy = ''  #Name of the player that challenged him. Default none

    def display(self):
        '''Returns info about the trainer'''
        mess = ''
        mess += self.name + '(' + str(self.x) + ', ' + str(self.y) + ') - Score:' + str(self.score) + '\n'
        mess += 'Kudomons:\n'
        for kudomon in self.kudomons:   #info about the Kudomons
            mess += '\t' + kudomon.display() + '\n'
        return mess

    def displayKudomons(self):
        '''Returns info about owned Kudomons'''
        mess = 'Kudomons:\n'
        for kudomon in self.kudomons:
            mess += '\t' + kudomon.display() + '\n'
        return mess

    def move(self, direction):
        '''X is left / right, Y is up / down'''
        if direction == 'up':
            self.y = max(0, self.y - 1)
        elif direction == 'right':
            self.x = min(100, self.x + 1)
        elif direction == 'down':
            self.y = min(100, self.y + 1)
        elif direction == 'left':
            self.x = max(0, self.x - 1)

class MyServer(Server):
    def onStart(self):
        print 'Server started'
        self.kudomon_names = ['Ace','Apollo','Bailey','Bandit','Baxter','Bear','Beau','Benji','Benny','Bentley','Blue','Bo','Boomer','Brady','Brody','Bruno','Brutus','Bubba','Buddy','Buster','Cash','Champ','Chance','Charlie','Chase','Chester','Chico','Coco','Cody','Cooper','Copper','Dexter','Diesel','Duke','Elvis','Finn','Frankie','George','Gizmo','Gunner','Gus','Hank','Harley','Henry','Hunter','Jack','Jackson','Jake','Jasper','Jax','Joey','Kobe','Leo','Loki','Louie','Lucky','Luke','Mac','Marley','Max','Mickey','Milo','Moose','Murphy','Oliver','Ollie','Oreo','Oscar','Otis','Peanut','Prince','Rex','Riley','Rocco','Rocky','Romeo','Roscoe','Rudy','Rufus','Rusty','Sam','Sammy','Samson','Scooter','Scout','Shadow','Simba','Sparky','Spike','Tank','Teddy','Thor','Toby','Tucker','Tyson','Vader','Winston','Yoda','Zeus','Ziggy']
        self.kudomon_types = ['water', 'fire', 'grass', 'rock', 'electric', 'psihic']
        #intiailize dict of players
        self.players = {}
        #intialize dict of kudomons (based on location)
        self.kudomons = {}
        #intialize inRange (Kudomons) list
        self.inRange = []
        #A map of 101x101
        self.map = [[0 for j in range(101)] for i in range(101)]
        #Add 72 Kudomons to the map, making sure no 2 Kudomons share the same space
        for i in range(72):
            while True:
                x = randint(0, 100)
                y = randint(0, 100)
                if str(str(x) + ',' + str(y)) not in self.kudomons:
                    self.kudomons[str(str(x) + ',' + str(y))] = Kudomon(random.choice(self.kudomon_names), random.choice(self.kudomon_types), x, y)
                    break
        #Print the Kudomons on the server side so you can cheat in catching them (by seeing their position)
        for i in range(101):
            for j in range(101):
                if str(str(i) + ',' + str(j)) in self.kudomons:
                    print ('Kudomon(' + str(i) + ', ' + str(j) + '): ' + self.kudomons[str(str(i) + ',' + str(j))].display())

    def onStop(self):
        print 'Server stopped'

    def onConnect(self, socket):
        print 'Connected'
        socket.screenName = None

    def onDisconnect(self, socket):
        print 'Disconnected'
        del self.players[socket.screenName]

    def onMessage(self, socket, message):
        #sometimes useful
        (command, sep, parameter) = message.strip().partition(' ')

        #helped in debugging
        print 'Message is ', message

        #register new user. this message will be automatically sent each time you connect to the server
        if command == 'REGISTER':
            socket.screenName = parameter
            self.players[socket.screenName] = Player(socket, socket.screenName)
            self.players[socket.screenName].display();

        if socket.screenName in self.players:
            if self.players[socket.screenName].challenged == False:
                if command == 'status':
                    '''Info about the all players and their Kudomons'''
                    for player in self.players:
                        self.players[socket.screenName].socket.send(("%s\n" % self.players[player].display().strip()).encode('utf-8'))
                elif command == 'move':
                    '''Move up / right / down / left and clean inRange list'''
                    self.players[socket.screenName].move(parameter)
                    socket.send(self.players[socket.screenName].display())
                    self.inRange = []
                elif command == 'nearby':
                    '''In range: in a range of 3x3
                       Close: in a range of 7x7
                       Nearby: in a range of 10x10
                            Add in range kudomons to inRange list'''
                    mess = 'In range:\n'
                    for i in range(self.players[socket.screenName].x - 3, self.players[socket.screenName].x + 3):
                        for j in range(self.players[socket.screenName].y - 3, self.players[socket.screenName].y + 3):
                            if str(str(i) + ',' + str(j)) in self.kudomons:
                                mess += '\t' + self.kudomons[str(str(i) + ',' + str(j))].display() + '\n'
                                self.inRange.append(self.kudomons[str(str(i) + ',' + str(j))])
                    mess += 'Close:\n'
                    for i in range(self.players[socket.screenName].x - 7, self.players[socket.screenName].x + 7):
                        for j in range(self.players[socket.screenName].y - 7, self.players[socket.screenName].y + 7):
                            if j not in range(self.players[socket.screenName].y - 3, self.players[socket.screenName].y + 3) or i not in range(self.players[socket.screenName].x - 3, self.players[socket.screenName].x + 3):
                                if str(str(i) + ',' + str(j)) in self.kudomons:
                                    mess += '\t' + self.kudomons[str(str(i) + ',' + str(j))].display() + '\n'
                    mess += 'Nearby:\n'
                    for i in range(self.players[socket.screenName].x - 10, self.players[socket.screenName].x + 10):
                        for j in range(self.players[socket.screenName].y - 10, self.players[socket.screenName].y + 10):
                            if j not in range(self.players[socket.screenName].y - 7, self.players[socket.screenName].y + 7) or i not in range(self.players[socket.screenName].x - 7, self.players[socket.screenName].x + 7):
                                if str(str(i) + ',' + str(j)) in self.kudomons:
                                    mess += '\t' + self.kudomons[str(str(i) + ',' + str(j))].display() + '\n'
                    #self.players[socket.screenName].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                    socket.send(mess)   #realized this method exists...
                elif command == 'catch':
                    '''If Kudomons are in range, catch one at random.'''
                    if len(self.inRange) == 0:
                        socket.send('Nothing to catch!')
                    else:
                        kudomon = random.choice(self.inRange)
                        for key in self.kudomons:
                            if kudomon == self.kudomons[key]:
                                del self.kudomons[key]
                                break
                        kudomon.owner = socket.screenName
                        self.players[socket.screenName].kudomons.append(kudomon)
                        socket.send(self.players[socket.screenName].displayKudomons())
                elif command == 'challenge' and len(self.players[socket.screenName].kudomons) > 0:
                    '''If you have Kudomons, you can challenge other players'''
                    if parameter in self.players:
                        self.players[parameter].challenged = True
                        self.players[parameter].challengedBy = socket.screenName
                        self.players[parameter].socket.send(("%s\n" % (socket.screenName + ' has challenged you. Do you accept? (yes / no)').strip()).encode('utf-8'))
            else:
                if command == 'yes' and len(self.players[socket.screenName].kudomons) > 0:
                    '''If you have been challenged, you have to select either yes or no to accept or deny the challenge. Fight will commence shortly'''
                    self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % (socket.screenName + ' has accepted your challenge:\n').strip()).encode('utf-8'))

                    A = random.choice(self.players[socket.screenName].kudomons) #random Kudomon from this trainer
                    B = random.choice(self.players[self.players[socket.screenName].challengedBy].kudomons)  #random Kudomon from the other trainer

                    #save some variables for calculating the score
                    aHP = A.hp
                    aCP = A.cp
                    bHP = B.hp
                    bCP = B.cp

                    if randint(0,9) < 5:    #Randomly decide who attacks first
                        '''One of the Kudomons goes first. If the other one has HP left, the other one will attack the first one.'''
                        '''If the first one has HP left, it will repeat. When a Kudomon has been knocked out, the fight will end and the winner will be decided (the Kudomon still standing, obviously).'''
                        '''The score is calculated based on the stats of the 2 fighting Kudomons in order to demotivate high-level players attacking newbies. #mechanics'''
                        while True:
                            mess = A.fight(B)
                            self.players[socket.screenName].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                            self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                            if B.hp <= 0:
                                self.players[socket.screenName].socket.send(("%s\n" % ('You won the fight!').strip()).encode('utf-8'))
                                self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % ('You lost the fight!').strip()).encode('utf-8'))
                                self.players[socket.screenName].score += (5 + (bHP * bCP - aHP * aCP) / 1000)
                                self.players[self.players[socket.screenName].challengedBy].kudomons.remove(B)
                                break;
                            else:
                                mess = B.fight(A)
                                self.players[socket.screenName].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                                self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                                if A.hp <= 0:
                                    self.players[socket.screenName].socket.send(("%s\n" % ('You lost the fight').strip()).encode('utf-8'))
                                    self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % ('You won the fight!').strip()).encode('utf-8'))
                                    self.players[self.players[socket.screenName].challengedBy].score += (5 + (aHP * aCP - bHP * bCP) / 1000)
                                    self.players[socket.screenName].kudomons.remove(A)
                                    break;
                    else:
                        while True:
                            mess = B.fight(A)
                            self.players[socket.screenName].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                            self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                            if A.hp <= 0:
                                self.players[socket.screenName].socket.send(("%s\n" % ('You lost the fight').strip()).encode('utf-8'))
                                self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % ('You won the fight!').strip()).encode('utf-8'))
                                self.players[self.players[socket.screenName].challengedBy].score += (5 + (aHP * aCP - bHP * bCP) / 1000)
                                self.players[socket.screenName].kudomons.remove(A)
                                break;
                            else:
                                mess = A.fight(B)
                                self.players[socket.screenName].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                                self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % mess.strip()).encode('utf-8'))
                                if B.hp <= 0:
                                    self.players[socket.screenName].socket.send(("%s\n" % ('You won the fight!').strip()).encode('utf-8'))
                                    self.players[self.players[socket.screenName].challengedBy].socket.send(("%s\n" % ('You lost the fight!').strip()).encode('utf-8'))
                                    self.players[socket.screenName].score += (5 + (bHP * bCP - aHP * aCP) / 1000)
                                    self.players[self.players[socket.screenName].challengedBy].kudomons.remove(B)
                                    break;
                    self.players[socket.screenName].challenged = False  #after fight, player no longer challenged. Hopefully.
                else:
                    self.players[socket.screenName].challenged = False  #if the fight has veen avoided

        #socket.send(message)
        return True

ip = sys.argv[1]    #get IP
port = int(sys.argv[2]) #get Port

server = MyServer()

server.start(ip, port)
