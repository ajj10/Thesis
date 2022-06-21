class Player:
  def __init__(self, id, name, isServer):
    self.id = id
    self.name = name
    self.isServer = isServer
    self.key = "inv(pk({}))".format(name)
    self.knowledge = [self.key]

  def addToKnowledge(self,msg):
    self.knowledge.append(msg)

  def pretty(self):
    return self.name
  