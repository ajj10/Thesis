class FexchangeR:
  def __init__(self, me1, hash):
    self.me1 = me1
    self.hash = hash
    self.type = "exchangeR" 

  def pretty(self):
    return "f_exchangeR({},{})".format(self.me1.pretty(),self.hash)