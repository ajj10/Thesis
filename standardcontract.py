class Standardcontract:
  def __init__(self, me1, o_O, me2, o_R):
    self.me1 = me1
    self.me2 = me2
    self.o_O = o_O 
    self.o_R = o_R
    self.type = "standard_contract" 

  def pretty(self):
    return "({}, {}, {}, {})".format(self.me1.pretty(), self.o_O, self.me2.pretty(), self.o_R)