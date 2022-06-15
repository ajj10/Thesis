from fexchangeI import FexchangeI
from fexchangeR import FexchangeR
from abort import Abort
from sign import Sign
from contract import Contract

def addToCrimes(culprit,crimes,crime):
    if crime not in crimes[culprit]:
        crimes[culprit].append(crime)