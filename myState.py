from myLaws import *

class MyState:
    def __init__(self, players, LRS):
        self.msgTrace = [] # message trace of the state
        self.msgNetwork = [] # all messages on the network
        self.knownContracts = [] # contracts known to server, bulletin board (replaced or aborted)
        self.knownStandardContracts = [] # standard contracts unknown to server T
        # contracts players have signed (Players should remeber contract they have signed)
        self.playerContracts = {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []} 
        self.players = players # all players in the system
        # initial knowledge of all players
        self.playersKnowledge = {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []} 
        # Record of players and the crimes they have commited if any
        self.crimes = {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []} 
        self.LRS = LRS # List of legally recognized servers
        self.type = "state" 

        # checking if a player has leaked his private key
        law2(self)

        # Adding players knowledge to the states players knowledge
        for player in self.players:
            self.playersKnowledge[player.name] = self.playersKnowledge[player.name] + player.knowledge

    # adding a message to the state, it adds the message to both players knowledge, to the network,
    # adds it to the states message trace and checks if any laws are broken.
    def addMsg(self, msg):
        players = []
        players.append(msg.originator)
        players.append(msg.recevier)
        message = msg.message
        self.msgTrace.append(msg)
        # A standard contract is not a message but rather a set of messages players can comppute
        # after a round of the CS protocol, so no check of the messages is needed here
        # this just replicates a succsessfull run of the protocol
        if(message.type=="standard_contract"):
            # add the contract to the known standard contracts withing the state
            self.knownStandardContracts.append(message.me1.message.text)
            tmp = []
            # checks if message is valid
            try:
                tmp.append(message.o_O)
                tmp.append(message.o_R)
                tmp.append(msg)
            # Otherwise signing player becomes a culprit in the state
            except:
                print("An exception occurred")
            # add the new message to players knowledge and to the set of message on the network
            self.addPlayersKnowledge(tmp, players)
        elif(message.message.type=="exchangeI"):
            tmp = []
            # checks if message is valid
            try:
                tmp.append(msg)
            # Otherwise signing player becomes a culprit in the state
            except:
                addToCrimes(message.signer.name, self.crimes, "signing an invalid message")
            # add the new message to players knowledge and to the set of message on the network
            self.addPlayersKnowledge(tmp, players)   
            law6(self) # checking me_1
            # add the contract to the players known contracts (illegal to sign the same contract again)
            self.playerContracts[message.signer.name].append(message.message.text)
        elif(message.message.type=="exchangeR"):
            tmp = []
            # checks if message is valid
            try:
                tmp.append(msg)
                msg.message.message.me1.message.originator
            # Otherwise signing player becomes a culprit in the state
            except:
                addToCrimes(message.signer.name, self.crimes, "Law 7.1: signing an invalid message")
                return
            # add the new message to players knowledge and to the set of message on the network
            self.addPlayersKnowledge(tmp, players)
            law7(self) # checking me_2
            # add the contract to the players known contracts (illegal to sign the same contract again)
            self.playerContracts[message.signer.name].append(message.message.me1.message.text)
        elif(message.message.type=="abort"):
            tmp = []
            # checks if message is valid
            try:
                tmp.append(msg)
                msg.message.message.me1.message.originator
            # Otherwise signing player becomes a culprit in the state
            except:
                addToCrimes(message.signer.name, self.crimes, "Law 8.1: Signing an invalid message")
                return
            # add the new message to players knowledge and to the set of message on the network
            self.addPlayersKnowledge(tmp, players)
            law8(self) # checking ma_1
        elif(message.message.type=="aborted"):
            tmp = []
            # checks if message is valid
            try:
                tmp.append(msg)
                message.message.ma1.message.me1.message.text.aborted
            # Otherwise signing player becomes a culprit in the state
            except:
                addToCrimes(message.signer.name, self.crimes, "Law 9.1: Signing an invalid message")
                return   
            # add the new message to players knowledge and to the set of message on the network
            self.addPlayersKnowledge(tmp, players)
            # marking the contract as aborted, illegal to replace it after that  
            message.message.ma1.message.me1.message.text.aborted = True
            # add the contract to the states known contracts (all contracts on bulltin board, aborted or replaced)
            self.knownContracts.append(message.message.ma1.message.me1.message.text)
            law9(self) # checking ma_2
        elif(message.message.type=="replacement"):
            tmp = []
            # checks if message is valid
            try:
                tmp.append(msg)
                message.message.me1.message.text.replacement
                msg.message.message.me2.message
            # Otherwise signing player becomes a culprit in the state
            except:
                addToCrimes(message.signer.name, self.crimes, "Law 10.1/10.2: Signing an invalid message")
                return
            # add the new message to players knowledge and to the set of message on the network
            self.addPlayersKnowledge(tmp, players)
            # marking the contract as replaced, illegal to abort it after that           
            message.message.me1.message.text.replacement = True
            # add the contract to the states known contracts (all contracts on bulltin board, aborted or replaced)
            self.knownContracts.append(message.message.me1.message.text)
            law10(self) # checking replacement contract

    # add the new message to players knowledge and to the set of message on the network
    # (in theory, the sending player would already have this in his knowledge)
    def addPlayersKnowledge(self, tmp, players):
        for n in tmp:
            for player in players:
                if n not in self.playersKnowledge[player.name]:
                    self.playersKnowledge[player.name].append(n)
                    player.addToKnowledge(n)
                    self.msgNetwork.append(n)
        
            