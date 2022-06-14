class Contract:
  def __init__(self, id, originator, receiver, contractText):
    self.signer = id
    self.originator = originator
    self.receiver = receiver
    self.contractText = contractText
    self.aborted = False
    self.replacement = False
    self.type = "contract"
  
  def pretty(self):
    return self.contractText