from fexchangeI import FexchangeI
from fexchangeR import FexchangeR
from abort import Abort
from sign import Sign
from contract import Contract

# Hash function
def h(nonce):
    return "h"+nonce[1]

# function to check if a signiture on a message of f_exchangeI format is legal
def fexchangeIcheck(evidence, knownContracts, LRS, players, stdContract):
    if(evidence.signer.id == evidence.message.originator.id):
        if((evidence.message.recevier in players)):
            if(evidence.message.server in LRS):
                if(type(evidence.message.text)==Contract):
                    if(type(evidence.message.hash)==str):
                        print("legal message")
                        if(stdContract):
                            knownContracts.append(evidence.message.text)
                    else:
                        print("h_O is not a hash, culprit: {}".format(evidence.signer.name))
                else:
                    print("text is not a contract, culprit: {}".format(evidence.signer.name))
            else:
                print("T not in LRS, culprit: {}".format(evidence.signer.name))
        else:
            print("incorrect variable type for recipient, culprit: {}".format(evidence.signer.name))
    else:
        print("incorrect originator, culprit: {}".format(evidence.signer.name))

# function to check if a signiture on a message of f_exchangeR format is legal
def fexchangeRcheck(evidence, knownContracts, LRS):
    if(type(evidence.message.me1) == Sign):
        if(type(evidence.message.me1.message) == FexchangeI):
            if(evidence.message.me1.signer == evidence.message.me1.message.originator):
                if(evidence.signer == evidence.message.me1.message.recevier):
                    if(evidence.message.me1.message.server in LRS):
                        if(type(evidence.message.me1.message.text)==Contract):
                            if(type(evidence.message.hash)==str):
                                print("legal message")
                            else:
                                print("h_R is not a hash, culprit: {}".format(evidence.signer.name))
                        else:
                            print("text is not a contract, culprit: {}".format(evidence.signer.name))
                    else:
                        print("T not in LRS, culprit: {}".format(evidence.signer.name))
                else:
                    print("incorrect recipient, culprit: {}".format(evidence.signer.name))
            else:
                print("incorrect originator, culprit: {}".format(evidence.signer.name))
        else:
            print("invalid me_1 message, culprit: {}".format(evidence.signer.name))
    else:
        print("unsigned me_1 message, culprit: {}".format(evidence.signer.name))

# function to check if a signiture on a message of f_abort format is legal
def abortcheck(evidence, nonce, knownContracts, LRS):
    if(type(evidence.message.me1) == Sign):
        if(type(evidence.message.me1.message) == FexchangeI):
            if(evidence.message.me1.signer == evidence.message.me1.message.originator and evidence.signer==evidence.message.me1.signer):
                if(evidence.message.me1.message.server in LRS):
                    if(type(evidence.message.me1.message.text)==Contract):
                        if(nonce!=None):
                            if(evidence.message.me1.message.hash != str(h(nonce))):
                                print("legal message")
                                evidence.message.me1.message.text
                            else:
                                print("known nonce, culprit: {}".format(evidence.signer.name))
                        else:
                            if(evidence.message.me1.message.text not in knownContracts):
                                print("legal message")
                            else:
                                if(evidence.message.me1.message.originator == evidence.message.me1.message.text.originator and evidence.message.me1.message.recevier == evidence.message.me1.message.text.receiver):
                                    print("re-used contract, culprit: {}".format(evidence.signer.name))
                                else: 
                                    print("legal message(contract known, but different players)")
                    else:
                        print("text is not a contract, culprit: {}".format(evidence.signer.name))
                else:
                    print("T not in LRS, culprit: {}".format(evidence.signer.name))
            else:
                print("incorrect originator, culprit: {}".format(evidence.signer.name))
        else:
            print("invalid me_1 message, culprit: {}".format(evidence.signer.name))
    else:
        print("unsigned me_1 message, culprit: {}".format(evidence.signer.name))

# function to check if a signiture on a message of f_aborted format is legal
def abortedcheck(evidence, knownContractsT, LRS):
    if(type(evidence.message.ma1) == Sign):
        if(type(evidence.message.ma1.message) == Abort):
            if(evidence.message.ma1.signer == evidence.message.ma1.message.me1.signer and evidence.message.ma1.message.me1.signer==evidence.message.ma1.message.me1.message.originator):
                if(evidence.signer in LRS):
                    if(evidence.signer == evidence.message.ma1.message.me1.message.server):
                        if(type(evidence.message.ma1.message.me1.message.text)==Contract):
                            if(evidence.message.ma1.message.me1.message.text not in knownContractsT):
                                print("legal message")
                                knownContractsT.append(evidence.message.ma1.message.me1.message.text)
                                evidence.message.ma1.message.me1.message.text.aborted = True
                            else:
                                if(evidence.message.ma1.message.me1.message.originator == evidence.message.ma1.message.me1.message.text.originator and evidence.message.ma1.message.me1.message.recevier == evidence.message.ma1.message.me1.message.text.receiver):
                                    if(evidence.message.ma1.message.me1.message.text.replacement):
                                        print("replacement contract exists, culprit: {}".format(evidence.signer.name))
                                else: 
                                    print("legal message(contract known, but different players or already aborted)")
                        else:
                            print("text is not a contract, culprit: {}".format(evidence.signer.name))
                    else: 
                        print("incorrect server, culprit: {}".format(evidence.signer.name))
                else:
                    print("T not in LRS, culprit: {}".format(evidence.signer.name))
            else:
                print("incorrect originator, culprit: {}".format(evidence.signer.name))
        else:
            print("invalid ma_1 message, culprit: {}".format(evidence.signer.name))
    else:
        print("unsigned ma_1 message, culprit: {}".format(evidence.signer.name))

# function to check if a signiture on a message of f_replacement format is legal
def replacementcheck(evidence, knownContractsT, LRS):
    if(type(evidence.message.me1) == Sign and type(evidence.message.me2) == Sign and type(evidence.message.me2.message) == FexchangeR and type(evidence.message.me2.message.me1) == Sign):
        if(type(evidence.message.me1.message) == FexchangeI and type(evidence.message.me2.message) == FexchangeR):
            if(evidence.message.me1.signer == evidence.message.me1.message.originator):
                if(evidence.message.me2.signer==evidence.message.me1.message.recevier):
                    if(evidence.signer in LRS):
                        if(evidence.signer == evidence.message.me1.message.server):
                            if(type(evidence.message.me1.message.text)==Contract):
                                if(evidence.message.me1.message.text not in knownContractsT):
                                    print("legal message")
                                    #knownContractsT.append(evidence.message.me1.message.text)
                                    evidence.message.me1.message.text.replacement = True
                                else:
                                    if(evidence.message.me1.message.originator == evidence.message.me1.message.text.originator and evidence.message.me1.message.recevier == evidence.message.me1.message.text.receiver):
                                        if(evidence.message.me1.message.text.aborted):
                                            print("abort token exists, culprit: {}".format(evidence.signer.name))
                                    else: 
                                        print("legal message(contract known, but different players)")
                            else:
                                print("text is not a contract, culprit: {}".format(evidence.signer.name))
                        else: 
                            print("incorrect server, culprit: {}".format(evidence.signer.name))
                    else:
                        print("T not in LRS, culprit: {}".format(evidence.signer.name))
                else:
                    print("incorrect receiver, culprit: {}".format(evidence.signer.name))
            else:
                print("incorrect originator, culprit: {}".format(evidence.signer.name))
        else:
            print("invalid me_1/me_2 message, culprit: {}".format(evidence.signer.name))
    else:
        print("unsigned me_1/me_2 message, culprit: {}".format(evidence.signer.name))

# function that takes in evidence and checks what kind of evidence is and if any laws have been broken
def checker(evidence, knownContracts, knownContractsT, LRS, players):
    evidence.display()
    if(evidence.stdcontract != None):
        print("checking me_1 message of standard contract:")
        fexchangeIcheck(evidence.stdcontract.me1,knownContracts,LRS,players, True)
        print("checking me_2 message of standard contract:")
        fexchangeRcheck(evidence.stdcontract.me2,knownContracts,LRS)
        print("-------------------------------------")
    for n in evidence.formatevidence:
        if(n.message.type == "exchangeI"):
            print("checking me_1 message:")
            fexchangeIcheck(n,knownContracts,LRS,players, False)
            print("-------------------------------------")
        if(n.message.type == "exchangeR"):
            print("checking me_2 message:")
            fexchangeRcheck(n,knownContracts,LRS)
            print("checking me_1 message:")
            if(type(n.message.me1)==Sign):
                if(type(n.message.me1.message)==FexchangeI):
                    fexchangeIcheck(n.message.me1,knownContracts,LRS,players, False)
                else:
                    print("invalid me_1 message, culprit: {}".format(n.message.me1.signer.name))
            else:
                print("unsigned me_1 message")
            print("-------------------------------------")
        elif(n.message.type == "abort"):
            print("checking ma_1 message:")
            abortcheck(n, evidence.nonce, knownContracts, LRS)
            print("checking me_1 message:")
            if(type(n.message.me1)==Sign):
                if(type(n.message.me1.message)==FexchangeI):
                    fexchangeIcheck(n.message.me1, knownContracts, LRS, players, False)
                else:
                    print("invalid me_1 message, culprit: {}".format(n.message.me1.signer.name))
            else:
                print("unsigned me_1 message")
            print("-------------------------------------")
        elif(n.message.type == "aborted"):
            print("checking ma_2 message:")
            abortedcheck(n, knownContractsT, LRS)
            print("checking ma_1 message:")
            if(type(n.message.ma1)==Sign):
                if(type(n.message.ma1.message)==Abort):
                    abortcheck(n.message.ma1, evidence.nonce, knownContracts, LRS)
                    print("checking me_1 message:")
                    if(type(n.message.ma1.message.me1)==Sign):
                        if(type(n.message.ma1.message.me1.message)==FexchangeI):
                            fexchangeIcheck(n.message.ma1.message.me1, knownContracts, LRS, players, False)
                            #knownContracts.append(n.message.ma1.message.me1.message.text)
                        else:
                            print("invalid me_1 message, culprit: {}".format(n.message.ma1.message.me1.signer.name))
                    else:
                        print("unsigned me_1 message")
                else:
                    print("invalid ma_1 message, culprit: {}".format(n.message.ma1.signer.name))
            else:
                print("unsigned ma_1 message")
            print("-------------------------------------")
        elif(n.message.type == "replacement"):
            print("checking f_replacement message:")
            replacementcheck(n, knownContractsT, LRS)
            print("checking me_2 message:")
            if(type(n.message.me2)==Sign):
                if(type(n.message.me2.message)==FexchangeR):
                    fexchangeRcheck(n.message.me2, knownContracts, LRS)
                else:
                    print("invalid me_2 message")
            else:
                print("unsigned me_2 message")
            print("checking me_1 message:")
            if(type(n.message.me1)==Sign):
                if(type(n.message.me1.message)==FexchangeI):
                    fexchangeIcheck(n.message.me1, knownContracts, LRS, players, False)
                    knownContracts.append(n.message.me1.message.text)
                else:
                    print("invalid me_1 message")
            else:
                print("unsigned me_1 message")
            print("-------------------------------------")
