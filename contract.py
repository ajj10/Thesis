class Contract:
  def __init__(self, id, originator, receiver, contractText):
    self.id = id
    self.originator = originator
    self.receiver = receiver
    self.contractText = contractText
    self.aborted = False
    self.replacement = False
    self.type = "contract"
  
  def abort(self):
    self.aborted = True

  def replace(self):
    self.replacement = True 
  
  def pretty(self):
    return self.contractText