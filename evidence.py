from replacement import Replacement
from aborted import Aborted
from standardcontract import Standardcontract
class Evidence:
    def __init__(self, id, evidence):
        self.nonce = None
        self.stdcontract = None
        self.abortToken = None
        self.replacementContract = None
        self.id = id
        self.type = "evidence"
        for n in evidence:
            try:
                if(type(n) is Standardcontract):
                    self.stdcontract = n
                    self.nonce = n.o_O
                elif(type(n.message) is Aborted):
                    self.abortToken = n
                elif(type(n.message) is Replacement):
                    self.replacementContract = n
                else:
                    print("invalid evidence")
                    exit()
            except:
                print("invalid evidence")
                exit()
                
        if self.abortToken is None:
            print("invalid evidence")
            exit()
        if self.replacementContract is None and self.stdcontract is None:
            print("invalid evidence")
            exit()
        if ((self.replacementContract is not None) and (self.stdcontract is not None)):
            print("invalid evidence")
            exit()
    
    def display(self):
        if self.stdcontract is not None:
            print("Evidence:\n Abort token: {} \n Contract: {}".format(self.abortToken.pretty(),self.stdcontract.pretty()))
        else:
            print("Evidence:\n Abort token: {} \n Contract: {}".format(self.abortToken.pretty(),self.replacementContract.pretty()))
        print("-------------------------------------------------------------")


