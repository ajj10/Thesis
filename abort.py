class Abort:
  def __init__(self, me1):
    self.me1 = me1
    self.type = "abort" 

  def pretty(self):
    return "f_abort({})".format(self.me1.pretty())