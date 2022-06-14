class MyMessage:
  def __init__(self, originator, recevier, message):
    self.originator = originator
    self.recevier = recevier
    self.message = message
    self.type = "message"

  def pretty(self):
    return self.message.pretty()