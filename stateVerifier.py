from fexchangeI import FexchangeI
from fexchangeR import FexchangeR
from abort import Abort
from aborted import Aborted
from replacement import Replacement
from sign import Sign
from player import Player
from contract import Contract
from standardcontract import Standardcontract
from evidence import Evidence
from myFunctions import *
from myState import MyState
from myMessage import MyMessage

# Players
players = []
O = Player(1, "O", False)
players.append(O)
R = Player(2, "R", False)
players.append(R)
T1 = Player(3, "T1", True)
players.append(T1)
T2 = Player(4, "T2", False)
players.append(T2)
T3 = Player(5, "T3", True)
players.append(T3)
X = Player(6, "X", False)
players.append(X)
Y = Player(7, "Y", False)
players.append(Y)
C = Player(8, "C", False)

# Legally Recognized Servers
LRS = []
for n in players:
    if n.isServer:
        LRS.append(n)

#contract, unique 
text1 = Contract(1, O, R, "text1")
text2 = Contract(2, O, R, "text2")
text3 = Contract(3, O, R, "text3")

# Known contracts, all contracts become know when servers handles them(posted on bulletin board)
# or when judge gets claim with the contract
knownContracts = []
knownContractsT = []
text2.replacement = True
text3.aborted = True
knownContractsT.append(text2) 
knownContractsT.append(text3) 

# Nonces
o_O = "oO"
o_R = "oR"

# Hashes
h_O = h(o_O)
h_R = h(o_R)

_ = None

# Crimes
crimes = {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': []}

#Law 2
def law2(state):
    for player in state.players:
        for k in state.playersKnowledge:
            if player.key in state.playersKnowledge[k] and player.name != k:
                crimes[player.name].append("Law #2: known private key")

#Law 6 - Possible law breaks
def law6(state):
    for k in state.playersKnowledge:
        for msg in state.playersKnowledge[k]:
            if(type(msg)!=str):
                if(msg.type!="standard_contract"):
                    if type(msg.message) is Sign:
                        if type(msg.message.message) is FexchangeI:
                            if(msg.message.signer.id == msg.message.message.originator.id):
                                if(msg.message.message.recevier in players):
                                    if(msg.recevier == msg.message.message.recevier):
                                        if(msg.message.message.server in LRS):
                                            if(type(msg.message.message.text)==Contract):
                                                if(type(msg.message.message.hash)==str):
                                                    "legal message"
                                                else:
                                                    crimes[msg.message.signer.name].append("Law #6: h_O is not a hash")
                                            else:
                                                crimes[msg.message.signer.name].append("Law #6: text is not a contract")
                                        else:
                                            crimes[msg.message.signer.name].append("Law #6: T not in LRS")
                                    else:
                                        crimes[msg.message.signer.name].append("Law #6: incorrect recipient")
                                else:
                                    crimes[msg.message.signer.name].append("Law #6: incorrect variable type for recipient")
                            else:
                                crimes[msg.message.signer.name].append("Law #6: incorrect originator")

def law7(state):
    for k in state.playersKnowledge:
        for msg in state.playersKnowledge[k]:
            if(type(msg)!=str):
                if(msg.type!="standard_contract"):
                    if type(msg.message) is Sign:
                        if type(msg.message.message) is FexchangeR:
                            if(msg.message.message.me1.signer == msg.message.message.me1.message.originator):
                                if(msg.message.signer == msg.message.message.me1.message.recevier):
                                    if(msg.message.message.me1.message.server in LRS):
                                        if(type(msg.message.message.me1.message.text)==Contract):
                                            if(type(msg.message.message.hash)==str):
                                                "legal message"
                                            else:
                                                crimes[msg.message.signer.name].append("Law #7: h_R is not a hash")
                                        else:
                                            crimes[msg.message.signer.name].append("Law #7: incorrect originator")
                                            print("text is not a contract, culprit: {}".format(msg.message.signer.name))
                                    else:
                                        crimes[msg.message.signer.name].append("Law #7: incorrect originator")
                                        print("T not in LRS, culprit: {}".format(msg.message.signer.name))
                                else:
                                    crimes[msg.message.signer.name].append("Law #7: incorrect originator")
                                    print("incorrect recipient, culprit: {}".format(msg.message.signer.name))
                            else:
                                crimes[msg.message.signer.name].append("Law #7: incorrect originator")
                                print("incorrect originator, culprit: {}".format(msg.message.signer.name))


def law8(state):
    for k in state.playersKnowledge:
        for msg in state.playersKnowledge[k]:
            if(type(msg)!=str):
                if(msg.type!="standard_contract"):
                    if type(msg.message) is Sign:
                        if type(msg.message.message) is Abort:
                            if(msg.message.message.me1.signer == msg.message.message.me1.message.originator and msg.message.signer==msg.message.message.me1.signer):
                                if(msg.message.message.me1.message.server in LRS):
                                    if(type(msg.message.message.me1.message.text)==Contract):
                                        for player in state.players:
                                            for n in state.playersKnowledge:
                                                if msg.message.message.me1.message.hash in state.playersKnowledge[n] and player.name != n:
                                                    print("known nonce, culprit: {}".format(msg.message.signer.name))
                                                    #msg.message.message.me1.message.text
                                                else:
                                                    print("law 8 not broken")
                                    else:
                                        print("text is not a contract, culprit: {}".format(msg.message.signer.name))
                                else:
                                    print("T not in LRS, culprit: {}".format(msg.message.signer.name))
                            else:
                                print("incorrect originator, culprit: {}".format(msg.message.signer.name))

def law9(state):
    for k in state.playersKnowledge:
        for msg in state.playersKnowledge[k]:
            if(type(msg)!=str):
                if(msg.type!="standard_contract"):
                    if type(msg.message) is Sign:
                        if type(msg.message.message) is Aborted:
                            if(msg.message.message.ma1.signer == msg.message.message.ma1.message.me1.signer and msg.message.message.ma1.message.me1.signer==msg.message.message.ma1.message.me1.message.originator):
                                if(msg.message.signer in LRS):
                                    if(msg.message.signer == msg.message.message.ma1.message.me1.message.server):
                                        if(type(msg.message.message.ma1.message.me1.message.text)==Contract):
                                            if(msg.message.message.ma1.message.me1.message.text not in knownContractsT):
                                                print("legal message")
                                                knownContractsT.append(msg.message.message.ma1.message.me1.message.text)
                                                msg.message.message.ma1.message.me1.message.text.aborted = True
                                            else:
                                                if(msg.message.message.ma1.message.me1.message.originator == msg.message.message.ma1.message.me1.message.text.originator and msg.message.message.ma1.message.me1.message.recevier == msg.message.message.ma1.message.me1.message.text.receiver):
                                                    if(msg.message.message.ma1.message.me1.message.text.replacement):
                                                        print("replacement contract exists, culprit: {}".format(msg.message.signer.name))
                                                else: 
                                                    print("legal message(contract known, but different players or already aborted)")
                                        else:
                                            print("text is not a contract, culprit: {}".format(msg.message.signer.name))
                                    else: 
                                        print("incorrect server, culprit: {}".format(msg.message.signer.name))
                                else:
                                    print("T not in LRS, culprit: {}".format(msg.message.signer.name))
                            else:
                                print("incorrect originator, culprit: {}".format(msg.message.signer.name))


me1_a = Sign(O, FexchangeI(O, R, T1, text1, h_O)) # legal message
me1_b = Sign(X, FexchangeI(O, R, T1, text1, h_O)) # illegal, breaks law 6.1 (X != O) 
me1_c = Sign(O, FexchangeI(O, C, T1, text1, h_O)) # illegal, breaks law 6.2 (C not in Player)
me1_d = Sign(O, FexchangeI(O, R, T2, text1, h_O)) # illegal, breaks law 6.3 (T2 not in server)
me1_e = Sign(O, FexchangeI(O, R, T1, O, h_O))     # illegal, breaks law 6.4 (text is not a valid contract)
me1_f = Sign(O, FexchangeI(O, R, T1, text1, X)) # illegal, breaks law 6.6 (h_O not a hash)

#Law 7 - Possible law breaks
me2_a = Sign(R, FexchangeR(me1_a, h_R)) # legal in all ways
me2_b = Sign(R, FexchangeR(FexchangeI(O, R, T1, text1, h_O), h_R)) # illegal, breaks law 7.1 (unsigned me1)
me2_c = Sign(R, FexchangeR(Sign(O, "tmp"), h_R)) # illegal, breaks law 7.1 (invalid me1)
me2_d = Sign(R, FexchangeR(me1_b, h_R)) # illegal, breaks law 7.2 (invalid originator) 
me2_e = Sign(X, FexchangeR(me1_a, h_R)) # illegal, breaks law 7.3 (invalid reciever)
me2_f = Sign(R, FexchangeR(me1_d, h_R)) # illegal, breaks law 7.4 (server not in LRS)
me2_g = Sign(R, FexchangeR(me1_e, h_R)) # illegal, breaks law 7.5 (text not a contract)
me2_h = Sign(R, FexchangeR(me1_a, X)) # illegal, breaks law 7.7 (h_O not a hash)

#Law 8 - Possible law breaks
ma1_a = Sign(O, Abort(me1_a)) # legal in all ways
ma1_b = Sign(O, Abort(FexchangeI(O, R, T1, text1, h_O))) # illegal, breaks law 8.1 (unsigned me1)
ma1_c = Sign(O, Abort(Sign(O, "tmp"))) # illegal, breaks law 8.1 (invalid me1)
ma1_d = Sign(O, Abort(me1_b)) # illegal, breaks law 8.2 (invalid originator) 
ma1_e = Sign(R, Abort(me1_a)) # illegal, breaks law 8.2 (invalid originator) 
ma1_f = Sign(O, Abort(me1_d)) # illegal, breaks law 8.3 (server not in LRS)
ma1_g = Sign(O, Abort(me1_e)) # illegal, breaks law 8.4 (text not a contract)

#Law 9 - Possible law breaks
ma2_a = Sign(T1, Aborted(ma1_a)) # legal in all ways
ma2_b = Sign(T1, Aborted(Abort(me1_a))) # illegal, breaks law 9.1 (unsigned ma1)
ma2_c = Sign(T1, Aborted(Sign(O, "tmp"))) # illegal, breaks law 9.1 (invalid ma1)
ma2_d = Sign(T1, Aborted(ma1_d)) # illegal, breaks law 9.2 (invalid originator)
ma2_e = Sign(T1, Aborted(ma1_e)) # illegal, breaks law 9.2 (invalid originator)
ma2_f = Sign(T2, Aborted(ma1_a)) # illegal, breaks law 9.3 (invalid server)
ma2_g = Sign(T3, Aborted(ma1_a)) # illegal, breaks law 9.4 (incorrect server)
ma2_h = Sign(T1, Aborted(ma1_g)) # illegal, breaks law 9.5 (text not a contract)
ma2_i = Sign(T1, Aborted(Sign(O, Abort(Sign(O, FexchangeI(O, R, T1, text2, o_O)))))) # illegal, breaks law 9.5 (replacement contract exists)

#Law 10 - Possible law breaks
rep_a = Sign(T1, Replacement(me1_a,me2_a)) # legal in all ways
rep_b = Sign(T1, Replacement(FexchangeI(O, R, T1, text1, h_O),me2_a)) # illegal, breaks law 10.1 (unsigned me1)
rep_c = Sign(T1, Replacement(Sign(O, "tmp"),me2_a)) # illegal, breaks law 10.1 (invalid me1)
rep_d = Sign(T1, Replacement(me1_a,FexchangeR(me1_a, h_R))) # illegal, breaks law 10.2 (unsigned me2)
rep_e = Sign(T1, Replacement(me1_a,Sign(O, "tmp"))) # illegal, breaks law 10.2 (invalid me2)
rep_f = Sign(T2, Replacement(me1_a,me2_a)) # illegal, breaks law 10.3 (T2 not in LRS)
rep_g = Sign(T3, Replacement(me1_a,me2_a)) # illegal, breaks law 10.4 (incorrcect server)
rep_h = Sign(T1, Replacement(me1_b,me2_a)) # illegal, breaks law 10.5 (X != O)
rep_i = Sign(T1, Replacement(me1_a,me2_e)) # illegal, breaks law 10.6 (X != R)
rep_j = Sign(T1, Replacement(me1_e,me2_g)) # illegal, breaks law 10.7 (text is not a contract)
rep_k = Sign(T1, Replacement(Sign(O, FexchangeI(O, R, T1, text3, o_O)),Sign(R, FexchangeR(Sign(O, FexchangeI(O, R, T1, text3, h_O)), h_R)))) # illegal, breaks law 10.7 (abort token exists on this contract)

#Valid standar contract
validContract = Standardcontract(me1_a, o_O, me2_a, o_R)

# Judge will get evidence of valid contract and abort, or a signed format message and possible a nonce
evid = Evidence(1, [ma2_a, rep_a])
#checker(evid, knownContracts, knownContractsT, LRS, players)

R.addToKnowledge(O.key)
R.addToKnowledge(o_O)


init_state = MyState(players)

me1_1 = MyMessage(O,R,me1_a)
me2_1 = MyMessage(R,O,me2_a)
ma1_1 = MyMessage(O,T1,ma1_a)
ma2_1 = MyMessage(T1,O,ma2_a)
rep_1 = MyMessage(T1,O,rep_a)
val_1 = MyMessage(O,R,validContract)

init_state.addMsg(me1_1)
init_state.addMsg(me2_1)
init_state.addMsg(ma1_1)
init_state.addMsg(ma2_1)
init_state.addMsg(rep_1)
init_state.addMsg(val_1)

#print(init_state.playersKnowledge)
law2(init_state)
law6(init_state)
law7(init_state)
law8(init_state)

print(crimes)
print(_)






