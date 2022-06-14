from aborted import Aborted
from abort import Abort
from fexchangeI import FexchangeI
from fexchangeR import FexchangeR
from replacement import Replacement


class MyState:
    def __init__(self, players):
        self.msgTrace = []
        self.msgNetwork = []
        self.knownContracts = [] #bulletin board
        self.players = players
        #self.playersKnowledge = dict.fromkeys([n.pretty() for n in players],[])
        self.playersKnowledge = {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': []}
        self.guiltyPlayers = []
        self.type = "state" 

        for player in self.players:
            self.playersKnowledge[player.name] = self.playersKnowledge[player.name] + player.knowledge

    def addMsg(self, msg):
        players = []
        players.append(msg.originator)
        players.append(msg.recevier)
        message = msg.message
        self.msgTrace.append(msg)
        for player in players:
            if(message.type=="standard_contract"):
                tmp = []
                tmp.append(message.pretty())
                tmp.append(message.me1.pretty())
                tmp.append(message.me1.message.originator.pretty())
                tmp.append(message.me1.message.recevier.pretty())
                tmp.append(message.me1.message.server.pretty())
                tmp.append(message.me1.message.text.pretty())
                tmp.append(message.me1.message.hash)
                tmp.append(message.o_O)
                tmp.append(message.me2.pretty())
                tmp.append(message.me2.message.me1.message.originator.pretty())
                tmp.append(message.me2.message.me1.message.recevier.pretty())
                tmp.append(message.me2.message.me1.message.server.pretty())
                tmp.append(message.me2.message.me1.message.text.pretty())
                tmp.append(message.me2.message.me1.message.hash)
                tmp.append(message.me2.message.hash)
                tmp.append(message.o_R)
                tmp.append(msg)
                for n in tmp:
                    if n not in self.playersKnowledge[player.name]:
                        self.playersKnowledge[player.name].append(n)
                        player.addToKnowledge(n)
                        self.msgNetwork.append(n)
            elif(message.message.type=="exchangeI"):
                tmp = []
                tmp.append(message.pretty())
                tmp.append(message.message.pretty())
                tmp.append(message.message.originator.pretty())
                tmp.append(message.message.recevier.pretty())
                tmp.append(message.message.server.pretty())
                tmp.append(message.message.text.pretty())
                tmp.append(message.message.hash)
                tmp.append(msg)
                for n in tmp:
                    if n not in self.playersKnowledge[player.name]:
                        self.playersKnowledge[player.name].append(n)
                        player.addToKnowledge(n)
                        self.msgNetwork.append(n)
            elif(message.message.type=="exchangeR"):
                tmp = []
                tmp.append(message.pretty())
                tmp.append(message.message.pretty())
                tmp.append(message.message.me1.pretty())
                tmp.append(message.message.me1.message.originator.pretty())
                tmp.append(message.message.me1.message.recevier.pretty())
                tmp.append(message.message.me1.message.server.pretty())
                tmp.append(message.message.me1.message.text.pretty())
                tmp.append(message.message.me1.message.hash)
                tmp.append(message.message.hash)
                tmp.append(msg)
                for n in tmp:
                    if n not in self.playersKnowledge[player.name]:
                        self.playersKnowledge[player.name].append(n)
                        player.addToKnowledge(n)
                        self.msgNetwork.append(n)
            elif(message.message.type=="abort"):
                tmp = []
                tmp.append(message.pretty())
                tmp.append(message.message.pretty())
                tmp.append(message.message.me1.pretty())
                tmp.append(message.message.me1.message.originator.pretty())
                tmp.append(message.message.me1.message.recevier.pretty())
                tmp.append(message.message.me1.message.server.pretty())
                tmp.append(message.message.me1.message.text.pretty())
                tmp.append(message.message.me1.message.hash)
                tmp.append(msg)
                for n in tmp:
                    if n not in self.playersKnowledge[player.name]:
                        self.playersKnowledge[player.name].append(n)
                        player.addToKnowledge(n)
                        self.msgNetwork.append(n)
            elif(message.message.type=="aborted"):
                self.knownContracts.append(message.message.ma1.message.me1.message.text)
                tmp = []
                tmp.append(message.pretty())
                tmp.append(message.message.pretty())
                tmp.append(message.message.ma1.pretty())
                tmp.append(message.message.ma1.message.me1.pretty())
                tmp.append(message.message.ma1.message.me1.message.originator.pretty())
                tmp.append(message.message.ma1.message.me1.message.recevier.pretty())
                tmp.append(message.message.ma1.message.me1.message.server.pretty())
                tmp.append(message.message.ma1.message.me1.message.text.pretty())
                tmp.append(message.message.ma1.message.me1.message.hash)
                tmp.append(msg)
                for n in tmp:
                    if n not in self.playersKnowledge[player.name]:
                        self.playersKnowledge[player.name].append(n)
                        player.addToKnowledge(n)
                        self.msgNetwork.append(n)
            elif(message.message.type=="replacement"):
                self.knownContracts.append(message.message.me1.message.text)
                tmp = []
                tmp.append(message.pretty())
                tmp.append(message.message.pretty())
                tmp.append(message.message.me1.pretty())
                tmp.append(message.message.me1.message.originator.pretty())
                tmp.append(message.message.me1.message.recevier.pretty())
                tmp.append(message.message.me1.message.server.pretty())
                tmp.append(message.message.me1.message.text.pretty())
                tmp.append(message.message.me1.message.hash)
                tmp.append(message.message.me2.pretty())
                tmp.append(message.message.me2.message.me1.message.originator.pretty())
                tmp.append(message.message.me2.message.me1.message.recevier.pretty())
                tmp.append(message.message.me2.message.me1.message.server.pretty())
                tmp.append(message.message.me2.message.me1.message.text.pretty())
                tmp.append(message.message.me2.message.me1.message.hash)
                tmp.append(message.message.me2.message.hash)
                tmp.append(msg)
                for n in tmp:
                    if n not in self.playersKnowledge[player.name]:
                        self.playersKnowledge[player.name].append(n)
                        player.addToKnowledge(n)
                        self.msgNetwork.append(n)
            