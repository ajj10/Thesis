class Replacement:
  def __init__(self, me1, me2):
    self.me1 = me1
    self.me2 = me2
    self.type = "replacement" 

  def pretty(self):
    return "f_replacement({},{})".format(self.me1.pretty(),self.me2.pretty())