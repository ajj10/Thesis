class Aborted:
  def __init__(self, ma1):
    self.ma1 = ma1
    self.type = "aborted" 

  def pretty(self):
    return "f_aborted({})".format(self.ma1.pretty())