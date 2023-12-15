import random  ## to generate the items
from pulp import * ## import pulp-or functions
import math
from .ISlave import *

'''
    Lo Slave problem trova il miglior pattern da utilizzare per 'partizionare' l'asse ( di dimensione maxValue ).
    In input riceve 
        - i valori duali computati dalla risoluzione del Restricted Master Problem
        - la dimensione l_i di ciascun tipo di unità da produrre
        - la dimensione L massima di un asse
'''
class SlaveProblem(ISlave):
    it = 0

    def __init__(self):
       pass

    '''
        Goal: Minimizzare il costo di produzione
        How: generare un pattern che abbia un valore di costo ridotto e contribuisca a ridurre il costo totale associato alle risorse utilizzate per produrre le unità richieste. 
        Sfrutto i costi ridotti generati dal RMP che indicano quanta variazione di costo si avrebbe per unità aggiuntiva di una determinata risorsa vincolante. 
    '''
    def setInitData(self,duals, itemLengths, maxValue,writeFile =True):
        self.duals = duals
        self.itemLengths = itemLengths
        self.maxValue = maxValue
        self.writeFile= writeFile

    def generatePattern(self):
        self.slaveprob=LpProblem("Slave solver",LpMinimize)

        '''
            Definizione delle variabili decisionali
                - S_00i : numero di unità della risorsa i 
            NOTA: S_{i:02d} -> I nomi generati hanno il prefisso 00
        '''
        self.varList=[
                LpVariable(
                    name= f'S_{i:02d}',
                    lowBound = 0,
                    upBound=None,
                    cat=LpInteger) 
            for i,x in enumerate(self.duals)]

        '''
            Utilizzo i valori duali nel calcolo dei coefficienti obiettivo dello Slave Problem
                -> Voglio massimizzare i reduced cost, cioè voglio che (1 - sum (duale *coeff)) sia massimo
                   - di conseguenza, voglio che il membro destro ( la somma sia quasi 0, cioè sia minima)
                   - quindi posso definire il problema come un max (sum (duale*coeff))
                     oppure anche min( -1 * sum(duale-coeff))
                   - moltiplico il valore duale per il numero di unità usate per quel tipo di taglio7
                   - massimizzo ()
        '''
        self.slaveprob.setObjective(
           -1 * lpSum([self.duals[i]*x for i, x in enumerate(self.varList)])
        )

        '''
            Definizione del vincolo:
                -> l_i * S_00i  + .... + l_n * S_00n <= L
                - Vincola lo slave a creare partizionamenti all'interno di un asse lungo  massimo L 
        '''
        self.slaveprob += LpConstraint(
            e=lpSum([self.itemLengths[i]*x for i, x in enumerate(self.varList)]),
            sense=LpConstraintLE,
            rhs=self.maxValue
        )
        if(self.writeFile):
            self.slaveprob.writeLP(f'models/slave/slaveprob{SlaveProblem.it}.lp')
        self.slaveprob.solve() 
        self.slaveprob.roundSolution() #to avoid rounding problems
        SlaveProblem.it: int=SlaveProblem.it+1

    '''
        Restituisce:
            -> l_i * S_00i  + .... + l_n * S_00n <= L
            -> Stiamo cercando il pattern che massimizza questo (1 - sum (duale *coeff))
            - di conseguenza, la funzione obiettivo ha calcolato il membro destro, e fornito i valori
              di un pattern. Però voglio che ('1- funzione obiettivo') sia grande. Cioè che 
              (valore soluzione) sia 0 o un valore molto negativo.
            - Vincola lo slave a creare partizionamenti all'interno di un asse lungo  massimo L 
    '''
    def returnPattern(self):
        pattern=False
        if self.slaveprob.objective is not None and value(self.slaveprob.objective) < -1.00001:
            pattern=[]
            for v in self.varList:
                pattern.append(value(v))
        return pattern
	
		
def testSlave():
    slave = SlaveProblem()
    slave.setInitData( [1.0, 1.0, 1.0],  [17, 12, 16], 25 )
    slave.generatePattern()
    print(slave.returnPattern())

testSlave()