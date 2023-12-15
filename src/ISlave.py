import random  ## to generate the items
from pulp import * ## import pulp-or functions

'''
    Interfaccia implementata dagli SlaveSolver - Column Generation.
'''
class ISlave:
    def setInitData(self,duals, itemLengths, maxValue):
        pass
    
    def generatePattern(self):
        pass
    
    def returnPattern(self):
        pass