from sign import Sign
class Req:
  def __init__(self, request, answer):
    self.request = request
    self.answer = answer
    self.type = "req" 

  def pretty(self):
    if type(self.request) is not Sign:
        return "req(({},{}),{})".format(self.request[0].pretty(),self.request[1].pretty(), self.answer)
    else:
        return "req({},{})".format(self.request.pretty(), self.answer)