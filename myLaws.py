from fexchangeI import FexchangeI
from fexchangeR import FexchangeR
from abort import Abort
from sign import Sign
from contract import Contract

# Hash function
def h(nonce):
    return "h"+nonce[-1]

def addToCrimes(culprit,crimes,crime):
    if crime not in crimes[culprit]:
        crimes[culprit].append(crime)

# Leaked private key
def law2(state):
    # for all players in the system
    for player in state.players:
        # for messages in respected players knowledge
        for k in state.playersKnowledge:
            # if the private key of a player is in another players knowledge
            if player.key in state.playersKnowledge[k] and player.name != k:
                addToCrimes(player.name, state.state.crimes, "Law #2: known private key")

# CS protocol initiation request (me_1)
def law6(state):
    # Take newest message of the trace
    msg=state.msgTrace[-1]
    # check if law 6.1 holds (O is correct originator)
    if(msg.message.signer.id != msg.message.message.originator.id):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.1: incorrect originator")
        addToCrimes(msg.message.signer.name, state.crimes, msg.message.pretty())
    # check if law 6.2 holds (R in Players)
    if(msg.message.message.recevier not in state.players):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.2: incorrect variable type for recipient")
    # check if law 6.3 holds (R is correct recevier)
    if(msg.recevier != msg.message.message.recevier):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.3: incorrect recipient")
    # check if law 6.4 holds (T in LRS) 
    if(msg.message.message.server not in state.LRS):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.4: T not in LRS")
    # check if law 6.5 holds (text is a contract)
    if(type(msg.message.message.text)!=Contract):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.5: text is not a contract")
    # check if law 6.5 holds (text is unique)
    if(msg.message.message.text in state.bulletinBoard):
            if msg.message.message.text.aborted:
                if msg.originator.name == msg.message.signer.name:
                    addToCrimes(msg.message.signer.name, state.crimes, "Law #7.5: contract already aborted")
    if(msg.message.message.text in state.playerContracts[msg.originator.name]):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.5: player has singned contract before")
    # check if law 6.6 holds (nonce is secret)
    for p in state.players:
        if p != msg.message.signer.name:
            for messages in state.playersKnowledge[p.name]:
                if(type(messages)==str and len(messages)>1):
                    if(msg.message.message.hash != messages and msg.message.message.hash == h(messages)):
                        if msg.originator.name == msg.message.signer.name:
                            addToCrimes(msg.message.signer.name, state.crimes, "Law #7.6: known hash")
    # check if law 6.7 holds (hash is a hash)
    if(type(msg.message.message.hash)!=str):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.7: h_O is not a hash")

# CS protocol initiation response (me_2)
def law7(state):
    # Take newest message of the trace
    msg=state.msgTrace[-1]
    # check if law 7.1 holds (Signed me_1)
    if type(msg.message.message.me1) is not Sign:
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.1: me_1 is not signed")
    # check if law 7.1 holds (me_1 is message of format f_exchangeI)
    if type(msg.message.message.me1.message) is not FexchangeI:
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.1: me_1 is not of format f_exhangeI")
    # check if law 7.2 holds (me_1 is signed by correct player(O))
    if(msg.message.message.me1.signer != msg.message.message.me1.message.originator):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.2: incorrect originator")
    # check if law 7.3 holds (R is the correct recipient)
    if(msg.message.signer != msg.message.message.me1.message.recevier):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.3: incorrect recipient")
    # check if law 7.4 holds (T in LRS)
    if(msg.message.message.me1.message.server not in state.LRS):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.4: T not in LRS")
    # check if law 7.5 holds (text is a contract)
    if(type(msg.message.message.me1.message.text)!=Contract):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.5: text is not a contract")
    # check if law 7.5 holds (text is a contract)
    if(msg.message.message.me1.message.text in state.playerContracts[msg.originator.name]):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #7.5: player has singned contract before")
    # check if law 7.6 holds (nonce is secret when signing f_exchangeR message)
    crimeFound = []
    for nonces in state.playersKnowledge[msg.message.signer.name]:
        if(type(nonces)==str and len(nonces)>1 and h(nonces)==msg.message.message.me1.message.hash):
            crimeFound =[]
            break
        else:
            for p in state.players:
                if p != msg.originator:
                    for messages in state.playersKnowledge[p.name]:
                        if(type(messages)==str and len(messages)>1):
                            if msg.message.message.hash == h(messages):
                                crimeFound.append(True)
    if len(crimeFound)>0:
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.6: known hash")
    # check if law 7.7 holds (hash is a hash)
    if(type(msg.message.message.hash)!=str):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #8.7: h_R is not a hash")
                                
# Abort request (ma_1)
def law8(state):
    # Take newest message of the trace
    msg=state.msgTrace[-1]
    # check if law 8.1 holds (Signed me_1)
    if type(msg.message.message.me1) is not Sign:
        addToCrimes(msg.message.signer.name, state.crimes, "Law #9.1: me_1 is not signed")
    # check if law 8.1 holds (me_1 is message of format f_exchangeI)
    if type(msg.message.message.me1.message) is not FexchangeI:
        addToCrimes(msg.message.signer.name, state.crimes, "Law #9.1: me_1 is not of format f_exhangeI")
    # check if law 8.2 holds (signer of ma_1 is same as signer of me_! and same as originator(O))
    if(msg.message.message.me1.signer != msg.message.message.me1.message.originator and msg.message.signer!=msg.message.message.me1.signer):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #9.2: incorrect originator/signer of me_1")
    # check if law 8.3 holds (T in LRS)
    if(msg.message.message.me1.message.server not in state.LRS):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #9.3: T not in LRS")
    # check if law 8.4 holds (text is a contract and O not signed it before this protocol run)
    if(type(msg.message.message.me1.message.text)!=Contract):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #9.4: text is not a contract")
    # check if law 8.5 holds (contract is unique)
    if(msg.message.message.me1.message.text in state.knownStandardContracts):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #9.5: same contract with same participants exists")

# Abort token (ma_2)
def law9(state):
    # Take newest message of the trace
    msg=state.msgTrace[-1]
    # check if law 9.1 holds (Signed ma_1)
    if type(msg.message.message.ma1) is not Sign:
        addToCrimes(msg.message.signer.name, state.crimes, "Law #10.1: ma_1 is not signed")
    # check if law 9.1 holds (me_1 is message of format f_abort)
    if type(msg.message.message.ma1.message) is not Abort:
        addToCrimes(msg.message.signer.name, state.crimes, "Law #10.1: me_1 is not of format f_abort")
    # check if law 9.2 holds (signiture on ma_1 and me_1 match O from f_exchangeI)
    if(msg.message.message.ma1.signer != msg.message.message.ma1.message.me1.signer and msg.message.message.ma1.message.me1.signer!=msg.message.message.ma1.message.me1.message.originator):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #10.2: incorrect originator/signer")
    # check if law 9.3 holds (T in LRS)
    if(msg.message.signer not in state.LRS):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #10.3: T not in LRS")
    # check if law 9.4 holds (T in f_exchangeI request)
    if(msg.message.signer != msg.message.message.ma1.message.me1.message.server):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #10.4: incorrect server")
    # check if law 9.5 holds (text is a contract)
    if(type(msg.message.message.ma1.message.me1.message.text)!=Contract):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #10.5: text is not a contract")
    # check if law 9.5 holds (text is unique and no replacement contract for it exists)
    if(msg.message.message.ma1.message.me1.message.text in state.bulletinBoard):
        if(msg.message.message.ma1.message.me1.message.text.replacement):
            addToCrimes(msg.message.signer.name, state.crimes, "Law #10.5: replacement contract exists")
            addToCrimes(msg.message.signer.name, state.crimes, msg.message.pretty())

# Replacement Contract 
def law10(state):
    # Take newest message of the trace
    msg=state.msgTrace[-1]
    # check if law 10.1/10.2 holds (Signed me_1 and me2)
    if(type(msg.message.message.me1) != Sign or type(msg.message.message.me2) != Sign):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #11.1/11.2: unsigned me_1/me_2")
    # check if law 10.1/10.2 holds (me_1 is of format f_exchangeI and me2 is of format f_exchangeR)
    if(type(msg.message.message.me1.message) != FexchangeI or type(msg.message.message.me2.message) != FexchangeR):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #11.1/11.2: me_1/me_2 is of wrong format")
    # check if law 10.3 holds (T in LRS)
    if(msg.message.signer not in state.LRS):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #11.3: T not in LRS")
    # check if law 10.4 holds (T in f_exchangeI request)
    if(msg.message.signer != msg.message.message.me1.message.server):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #11.4: incorrect server")
    # check if law 10.5 holds (Signer of me_1 is O from f_exchangeI)
    if(msg.message.message.me1.signer != msg.message.message.me1.message.originator):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #11.5: incorrect originator")
    # check if law 10.6 holds (Signer of me_2 is R from f_exchangeI)
    if(msg.message.message.me2.signer != msg.message.message.me1.message.recevier):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #11.6: incorrect receiver")
    # check if law 10.7 holds (text is a contract)
    if(type(msg.message.message.me1.message.text)!=Contract):
        addToCrimes(msg.message.signer.name, state.crimes, "Law #11.7: text is not a contract")
    # check if law 10.7 holds (text is unique and no abort token for it exists)
    if(msg.message.message.me1.message.text in state.bulletinBoard):               
        if(msg.message.message.me1.message.text.aborted):
            addToCrimes(msg.message.signer.name, state.crimes, "Law #11.7: abort token exists")
            addToCrimes(msg.message.signer.name, state.crimes, "Evid:{}".format(msg.message.pretty()))

def crimes(curr_state):
    print(curr_state.crimes)