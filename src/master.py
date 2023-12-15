
from pulp import * 
import math
from .ISlave import *


class MasterProblem():
	it = 0.

	'''
		Inizializza il problema principale
			- maxValue		  -> massima dimensione della tavola
			- itemLengths     -> vettore l_i: tipi di taglio da effettuare
			- itemDemands     -> vettore d_i : # minimo di tagli di tipo l_i richeisti
			- initialPatterns -> colonne iniziali da generare
			- slaveProblem    -> tipo di slave solver da utilizzare (Pulp Solver, GeneticAlgorithm)
		Definisce vincoli e variabili decisionali
	'''
	def __init__(self, maxValue, itemLengths, itemDemands, initialPatterns, slaveProblem:ISlave, writeLP=True):
		self.writeLP =writeLP
		self.slaveProblem :ISlave= slaveProblem
		self.maxValue=maxValue
		# Defines Aij
		self.itemLengths=itemLengths
		# Defines Bi
		self.itemDemands=itemDemands

		self.generatedPatterns=[]

		self.initialPatterns=initialPatterns
		self.PatternVars=[]
		self.constraintList=[]   
  

		self.prob = LpProblem('RMP',LpMinimize)	# set up the problem
		self.obj = LpConstraintVar("obj")   # generate a constraint variable that will be used as the objective
		self.prob.setObjective(self.obj)


		#********  Definizione variabili e vincoli  *************#

  		# Crea le variabili e imposta i vincoli, ovvero imposta la quantità minima di elementi da produrre
        # -> Ax >= b (Greater/Equal)
		for i,x in enumerate(itemDemands):		
			var=LpConstraintVar(
				name=f'C{i}',
				sense=LpConstraintGE,
				rhs=x
				) 
			self.constraintList.append(var)
			self.prob+=var
		  		
 		# Salva i pattern iniziali e imposta i vincoli di colonna cioè quante volte il pattern viene applicato
		for i,x in enumerate(self.initialPatterns):  
			affected_constraints = [j for j, y in enumerate(x) if y > 0]
 			# -> L'ultimo parametro del costruttore si riferisce all'esistenza della variabile nell'obiettivo e nei vincoli, il che significa che la variabile di decisione creata viene anche aggiunta alla formulazione del problema (nella funzione obiettivo).
			var = LpVariable( 
				name=f'Init_Pat{i}',
				lowBound= 0,
				upBound= None,
				cat= LpContinuous,
				e= lpSum(self.obj+[self.constraintList[v] for v in affected_constraints])
			)
			self.PatternVars.append(var)  
			self.generatedPatterns.append(x)
		if(self.writeLP):
			self.prob.writeLP('init_prob.lp')

		
		
	def solve(self):
		if(self.writeLP):
			self.prob.writeLP(f'models/master/prob{MasterProblem.it}.lp')
		MasterProblem.it+=1
		self.prob.solve()  # start solve
		
		return [self.prob.constraints[i].pi for i in self.prob.constraints]
		
			
	'''
		Aggiunge un nuovo pattern al modello esistente
	'''
	
	def addPattern(self,pattern):  
		#  indici dei vincoli influenzati da questo pattern 
		affected_constraints = [j for j, y in enumerate(pattern) if y > 0]
		# Ogni vincolo viene aggiornato
		# Ogni variabile nella colonna rappresenta il coefficiente di un vincolo corrispondente nella funzion
		# obiettivo.
		# ad es. 3*C2 + C4 + obj.
		# -> il nuovo pattern ha un coefficiente di 3 per il vincolo "C2", un coefficiente di 1
		# per il vincolo "C4". Di conseguenza, Pulp gestisce l'aggiornamento dei constraint C2 e C4,
		# aggiornandoli di conseguenza. 
		var = LpVariable(
		    	name=f'Pat{len(self.generatedPatterns)}',
				lowBound= 0, 
				upBound=None,
	            cat=LpContinuous,
				e=lpSum(self.obj+[pattern[v]*self.constraintList[v] for v in affected_constraints]))		
		self.generatedPatterns.append(pattern)
		self.PatternVars.append(var)
		
	'''
		Viene creato o avviato un nuovo slave problem (newSlaveProb) e vengono impostati i dati iniziali, come i 	duals, itemLengths e maxValue. Successivamente, viene generato un pattern utilizzando il metodo 		generatePattern() del problema slave e infine viene restituito il pattern ottenuto.
	'''
	def startSlave(self,duals):  # create/run new slave and return new pattern (if available)
		newSlaveProb=self.slaveProblem()
		newSlaveProb.setInitData(duals,self.itemLengths,self.maxValue)
		newSlaveProb.generatePattern()
		pattern=newSlaveProb.returnPattern()
  
		return pattern
	
	'''
		Viene utilizzato per impostare le variabili intere a False quando il parametro relaxed è False. In altre parole, se relaxed è False, le variabili vengono trattate come continue invece che come intere.
	'''
	def setRelaxed(self,relaxed):  
		if relaxed==False:
			for var in self.prob.variables():
				var.cat = LpInteger
			
	def getObjective(self):
		return value(self.prob.objective)
	
	'''
		Restituisce la lista dei pattern utilizzati nel modello, estraendone i valori.
		Viene verificato se il valore di una variabile di decisione x è maggiore di 0 e, in tal caso, viene aggiunto il valore e il pattern corrispondente alla lista usedPatternList.
	'''
	def getUsedPatterns(self):
		usedPatternList=[]
		for i,x in enumerate(self.PatternVars):
			if value(x)>0:
				usedPatternList.append((value(x),self.generatedPatterns[i]))
		return usedPatternList
	
	'''
		Estrae l'ottimo computato dal RMP,  arrotondato all'intero successivo utilizzando la funzione 
	'''
	def getComputedOptimal(self):
		status = LpStatus[self.prob.status]
		if status == 'Infeasible':
			return "Infeasible"
		return math.ceil(value(self.prob.objective))
	'''
		Recupera lo stato del master prob
	'''
	def getStatus(self):
		status = LpStatus[self.prob.status]
	
		return status