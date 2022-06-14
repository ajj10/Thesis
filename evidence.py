from standardcontract import Standardcontract
class Evidence:
    def __init__(self, id, evidence):
        self.nonce = None
        self.stdcontract = None
        self.formatevidence = []
        self.id = id
        self.type = "evidence"
        for n in evidence:
            if type(n)==str:
                self.nonce = n
            elif(type(n)==Standardcontract):
                self.stdcontract = n
                self.nonce = n.o_O
            else:
                self.formatevidence.append(n)
    
    def display(self):
        print("Evidence:")
        if(self.stdcontract != None):
            print("Standard contract: {}".format(self.stdcontract.pretty()))
        for k in self.formatevidence:
            try:
                if(k.message.type=="aborted"):
                    print("abort token: {})".format(k.pretty()))
                elif(k.message.type=="replacement"):
                    print("replacement contract: {})".format(k.pretty()))
            except:
                print("invalid message")
        print("-------------------------------------------------------------")


