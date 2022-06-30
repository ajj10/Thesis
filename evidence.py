from replacement import Replacement
from req import Req
from aborted import Aborted
from standardcontract import Standardcontract
class Evidence:
    def __init__(self, id, evidence):
        self.nonce = None
        self.stdcontract = None
        self.abortToken = None
        self.replacementContract = None
        self.id = id
        self.req = None
        self.type = "evidence"
        for n in evidence:
            if(type(n) is Req):
                self.req = n
                break
            try:
                print(type(n.message))
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
                
        if self.abortToken is None and self.req is None:
            print("invalid evidence")
            exit()
        elif self.replacementContract is None and self.stdcontract is None and self.req is None:
            print("invalid evidence")
            exit()
        elif ((self.replacementContract is not None) and (self.stdcontract is not None)):
            print("invalid evidence")
            exit()
    
    def display(self):
        if self.req is not None:
            print("Evidence:\n request: {}".format(self.req.pretty()))
            return
        if self.stdcontract is not None:
            print("Evidence:\n Abort token: {} \n Contract: {}".format(self.abortToken.pretty(),self.stdcontract.pretty()))
        else:
            print("Evidence:\n Abort token: {} \n Contract: {}".format(self.abortToken.pretty(),self.replacementContract.pretty()))
        print("-------------------------------------------------------------")


