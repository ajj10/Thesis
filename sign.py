class Sign:
  def __init__(self, signer, message):
    self.signer = signer
    self.message = message
    self.type = "sign"
  
  def pretty(self):
    try:
      return "sign(inv(pk({})),{})".format(self.signer.pretty(), self.message.pretty())
    except:
      return "invalid message"
