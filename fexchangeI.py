class FexchangeI:
  def __init__(self, originator, recevier, server, text, hash):
    self.originator = originator
    self.recevier = recevier
    self.server = server
    self.text = text
    self.hash = hash
    self.type = "exchangeI" 

  def pretty(self):
    return "f_exchangeI({},{},{},{},{})".format(self.originator.pretty(),self.recevier.pretty(),self.server.pretty(),self.text.pretty(),self.hash)

