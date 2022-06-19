from fexchangeI import FexchangeI
from fexchangeR import FexchangeR
from abort import Abort
from sign import Sign
from contract import Contract

# Hash function
def h(nonce):
    return "h"+nonce[-1]

# function to check if a signiture on a message of f_exchangeI format is legal
def fexchangeIcheck(evidence, LRS, players):
    #Start with an empty record where no one has broken any laws
    crimes= {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []}
    # check if law 6.1 holds (Signiture on me_1 matches O)
    if(evidence.signer != evidence.message.originator):
        crimes[evidence.signer.name].append("Law #6.1: incorrect originator")
    # check if law 6.2 holds (R in Players)
    if((evidence.message.recevier not in players)):
        crimes[evidence.signer.name].append("Law #6.2: incorrect variable type for recipient")
    # check if law 6.4 holds (T in LRS)
    if(evidence.message.server not in LRS):
        crimes[evidence.signer.name].append("Law #6.4: T not in LRS")
    # check if law 6.5 holds (text is a contract)
    if(type(evidence.message.text) is not Contract):
        crimes[evidence.signer.name].append("Law #6.5: text is not a contract")
    # check if law 6.7 holds (ho is a hash)
    if(type(evidence.message.hash) is not str):
        crimes[evidence.signer.name].append("Law #6.7: ho is not a hash")
    return crimes

# function to check if a signiture on a message of f_exchangeR format is legal
def fexchangeRcheck(evidence, LRS, players):
    #Start with an empty record where no one has broken any laws
    crimes= {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []}
    # check if law 7.1 holds (Signed me_1)
    if(type(evidence.message.me1) is not Sign):
        crimes[evidence.signer.name].append("Law #7.1: me_1 is not signed")
    # check if law 7.1 holds (me_1 is message of format f_exchangeI)
    try:
        if type(evidence.message.me1.message) is not FexchangeI:
            crimes[evidence.signer.name].append("Law #7.1: me_1 is not of format f_exchangeI")
            return crimes
    except:
        crimes[evidence.signer.name].append("Law #7.1: me_1 is not of format f_exchangeI")
        return crimes
    crimes = fexchangeIcheck(evidence.message.me1, LRS, players)
    # check if law 7.2 holds (signiture me_1 matches O from f_exchangeI)
    if(evidence.message.me1.signer != evidence.message.me1.message.originator):
        crimes[evidence.signer.name].append("Law #7.2: incorrect originator/signer")
    # check if law 7.3 holds (signer of me_2 matches R from me_1)
    if(evidence.signer != evidence.message.me1.message.recevier):
        crimes[evidence.signer.name].append("Law #7.3: incorrect recipient")
    # check if law 7.4 holds (T in LRS)
    if(evidence.message.me1.message.server not in LRS):
        crimes[evidence.signer.name].append("Law #7.4: T not in LRS")
    # check if law 7.5 holds (text is a contract)
    if(type(evidence.message.me1.message.text) is not Contract):
        crimes[evidence.signer.name].append("Law #7.5: text is not a contract")
    # check if law 7.7 holds (hash is a hash)
    if(type(evidence.message.me1.message.hash) is not str):
        crimes[evidence.signer.name].append("Law #7.7: hash is not a hash")
    return crimes


# function to check if a signiture on a message of f_abort format is legal
def abortcheck(evidence, nonces, knownContractsJudge, LRS, players):
    #Start with an empty record where no one has broken any laws
    crimes= {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []}
    # check if law 8.1 holds (Signed me_1)
    if(type(evidence.message.me1) is not Sign):
        crimes[evidence.signer.name].append("Law #8.1: me_1 is not signed")
    # check if law 8.1 holds (me_1 is message of format f_exchangeI)
    try:
        if type(evidence.message.me1.message) is not FexchangeI:
            crimes[evidence.signer.name].append("Law #8.1: me_1 is not of format f_exchangeI")
            return crimes
    except:
        crimes[evidence.signer.name].append("Law #8.1: me_1 is not of format f_exchangeI")
        return crimes
    crimes = fexchangeIcheck(evidence.message.me1, LRS, players)
    # check if law 8.2 holds (signiture on ma_1 and me_1 match O from f_exchangeI)
    if(evidence.message.me1.signer != evidence.message.me1.message.originator or evidence.signer != evidence.message.me1.signer):
        crimes[evidence.signer.name].append("Law #8.2: incorrect originator/signer")
    # check if law 8.3 holds (T in LRS)
    if(evidence.message.me1.message.server not in LRS):
        crimes[evidence.signer.name].append("Law #8.3: T not in LRS")
    # check if law 8.4 holds (text is a contract)
    if(type(evidence.message.me1.message.text)!=Contract):
        crimes[evidence.signer.name].append("Law #8.4: text is not a contract")
    # check if law 8.4 holds (text is unique)
    if(evidence.message.me1.message.text in knownContractsJudge):
        crimes[evidence.signer.name].append("Law #8.4: standard contract exists")
    # check if law 8.5 holds (nonce is secret)
    for nonce in nonces:
        if(evidence.message.me1.message.hash == str(h(nonce))):
            crimes[evidence.signer.name].append("Law #8.5: known nonce")
    return crimes

# function to check if a signiture on a message of f_aborted format is legal
def abortedcheck(evidence, nonces, knownContractsJudge, knownContractsT, LRS, players):
    #Start with an empty record where no one has broken any laws
    crimes= {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []}
    # check if law 9.1 holds (Signed ma_1)
    if type(evidence.abortToken.message.ma1) is not Sign:
        crimes[evidence.abortToken.signer.name].append("Law #9.1: ma_1 is not signed")
    # check if law 9.1 holds (ma_1 is message of format f_abort)
    try:
        if type(evidence.abortToken.message.ma1.message) is not Abort:
            crimes[evidence.abortToken.signer.name].append("Law #9.1: ma_1 is not of format f_abort")
            return crimes
    except:
        crimes[evidence.abortToken.signer.name].append("Law #9.1: ma_1 is not of format f_abort")
        return crimes
    crimes = abortcheck(evidence.abortToken.message.ma1, nonces, knownContractsJudge, LRS, players)
    # check if law 9.2 holds (signiture on ma_1 and me_1 match O from f_exchangeI)
    if(evidence.abortToken.message.ma1.signer != evidence.abortToken.message.ma1.message.me1.signer or evidence.abortToken.message.ma1.message.me1.signer!=evidence.abortToken.message.ma1.message.me1.message.originator):
        crimes[evidence.abortToken.signer.name].append("Law #9.2: incorrect originator/signer")
    # check if law 9.3 holds (T in LRS)
    if(evidence.abortToken.signer not in LRS):
        crimes[evidence.abortToken.signer.name].append("Law #9.3: T not in LRS")
    # check if law 9.4 holds (T in f_exchangeI request)
    if(evidence.abortToken.signer != evidence.abortToken.message.ma1.message.me1.message.server):
        crimes[evidence.abortToken.signer.name].append("Law #9.4: incorrect server")
    # check if law 9.5 holds (text is a contract)
    if(type(evidence.abortToken.message.ma1.message.me1.message.text)!=Contract):
        crimes[evidence.abortToken.signer.name].append("Law #9.5: text is not a contract")
    # check if law 9.5 holds (text is unique and no replacement contract for it exists)
    if(evidence.abortToken.message.ma1.message.me1.message.text in knownContractsT):
        if(evidence.abortToken.message.ma1.message.me1.message.text.replacement):
            crimes[evidence.abortToken.signer.name].append("Law #9.5: replacement contract exists")
    else:
        knownContractsT.append(evidence.abortToken.message.ma1.message.me1.message.text)
        evidence.abortToken.message.ma1.message.me1.message.text.aborted = True
    return crimes
    

# function to check if a signiture on a message of f_replacement format is legal
def replacementcheck(evidence, knownContractsT, LRS, players):
    #Start with an empty record where no one has broken any laws
    crimes= {'O': [], 'R': [], 'T1': [], 'T2': [], 'T3': [], 'X': [], 'Y': [], 'intruder': []}
    # check if law 10.1 holds (Signed me_1)
    if type(evidence.replacementContract.message.me1) is not Sign:
        crimes[evidence.replacementContract.signer.name].append("Law #10.1: me_1 is not signed")
    # check if law 10.2 holds (Signed me_2)
    if type(evidence.replacementContract.message.me2) is not Sign:
        crimes[evidence.replacementContract.signer.name].append("Law #10.2: me_2 is not signed")
    # check if law 10.1/10.2 holds (me_1/me_2 is of correct fomrat)
    try:
        if type(evidence.replacementContract.message.me1.message) is not FexchangeI:
            crimes[evidence.replacementContract.signer.name].append("Law #10.1: me_1 is not of format f_exchangeI")
            return crimes
        if type(evidence.replacementContract.message.me2.message) is not FexchangeR:
            crimes[evidence.replacementContract.signer.name].append("Law #10.2: me_2 is not of format f_exchangeR")
            return crimes
    except:
        crimes[evidence.replacementContract.signer.name].append("Law #10.1/10.2: me_1/me_2 is of wrong format")
        return crimes
    crimes = fexchangeRcheck(evidence.replacementContract.message.me2, LRS, players)
    # check if law 10.3 holds (T in LRS)
    if(evidence.replacementContract.signer not in LRS):
        crimes[evidence.replacementContract.signer.name].append("Law #10.3: T not in LRS")
    # check if law 10.4 holds (signer matches T from me_1)
    if(evidence.replacementContract.signer != evidence.replacementContract.message.me1.message.server):
        crimes[evidence.replacementContract.signer.name].append("Law #10.4: incorrect server")
    # check if law 10.5 holds (me_1 is signed by O from f_exchangeI)
    if(evidence.replacementContract.message.me1.signer != evidence.replacementContract.message.me1.message.originator):
        crimes[evidence.replacementContract.signer.name].append("Law #10.5: incorrect originator")
    # check if law 10.6 holds (me_2 is signed by R from fexchangeI)
    if(evidence.replacementContract.message.me2.signer != evidence.replacementContract.message.me1.message.recevier):
        crimes[evidence.replacementContract.signer.name].append("Law #10.6: incorrect recipient")
    # check if law 10.7 holds (text is a contract)
    if(type(evidence.replacementContract.message.me1.message.text) is not Contract):
        crimes[evidence.replacementContract.signer.name].append("Law #10.7: text not a contract")
    # check if law 10.7 holds (text is unique)
    if(evidence.replacementContract.message.me1.message.text in knownContractsT):
        if(evidence.replacementContract.message.me1.message.text.aborted):
            crimes[evidence.replacementContract.signer.name].append("Law #10.7: contract already aborted")
    else:
        knownContractsT.append(evidence.replacementContract.message.me1.message.text)
        evidence.replacementContract.message.me1.message.text.replacement = True
    return crimes

# function that takes in evidence and checks what kind of evidence it is and if any laws have been broken
def checkLawBreak(evidence, knownContractsJudge, knownContractsT, LRS, players):
    nonces = []
    if(evidence.stdcontract != None):
        nonces.append(evidence.stdcontract.o_O)
        nonces.append(evidence.stdcontract.o_R)
        print("checking me_1 message of standard contract:")
        crimes = fexchangeIcheck(evidence.stdcontract.me1,LRS,players)
        print(crimes)
        print("checking me_2 message of standard contract:")
        fexchangeRcheck(evidence.stdcontract.me2,LRS, players)
        print(crimes)
        knownContractsJudge.append(evidence.stdcontract.me1.message.text)
        print("-------------------------------------")
    else:
        print("checking replacement contract:")
        crimes = replacementcheck(evidence, knownContractsT, LRS, players)
        print(crimes)
        print("-------------------------------------")
    print("checking abort token:")
    crimes = abortedcheck(evidence, nonces, knownContractsJudge, knownContractsT, LRS, players)
    print(crimes)
    print("-------------------------------------")
