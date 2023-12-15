import random
from .ISlave import *
import math

'''
    Implementazione di un algoritmo genetico per generare un modello di 'taglio ottimo' utilizzando il concetto di pattern di taglio. Vengono utilizzate le variabili duali generate dalla risoluzione del Restricted Master Problem per guidare la generazione del pattern.

'''
class GeneticAlgorithm(ISlave):
    '''
        Iperparametri dell'algoritmo. 
    '''
    def __init__(self, population_size=5, generations=10):
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = 0.9
        self.mutation_rate = 0.15
    '''
        Il master problem inizializza ogni volta il GeneticAlgo fornendo i nuovi valori duali.
    '''
    def setInitData(self, duals, itemLengths, maxValue):
        self.duals = duals
        self.itemLengths = itemLengths
        self.maxValue = maxValue
        self.population = []

    

    def initialize_population(self):
        # Initialize the population with cutting patterns generated using the "first fit" heuristic
        for _ in range(self.population_size):
            chromosome = self.generate_first_fit_pattern()
            self.population.append(chromosome)

    '''
        Applica l'euristica del "first fit" per generare un pattern di taglio.
        In questo modo la prima generazione si trova in uno spazio di ricerca già più vicino a quello reale.
        Inoltre, lo shuffle permette di generare più pattern diversi 
        -> si rischia comunque che molti pattern siano uguali
    '''
    def generate_first_fit_pattern(self):
        # Apply the "first fit" heuristic to generate a cutting pattern
        pattern = [0] * len(self.itemLengths)  # Initialize the pattern with all zeros
        remaining_space = self.maxValue # Create a copy of item lengths
        
        indices = list(range(len(self.itemLengths)))
        random.shuffle(indices)

        for i in indices:
            if remaining_space >=self.itemLengths[i] :
                # Assign the item to the bin
                quantity = math.floor(remaining_space / self.itemLengths[i])
                pattern[i] += quantity
                remaining_space -= quantity * self.itemLengths[i]
            else:
                break
        return pattern


    '''
         Valuta la fitness di un 'cromosoma', calcolando la lunghezza totale dei tagli e utilizzando i valori duali per calcolare il punteggio di fitness.
         Siccome il valore di fittness viene utilizzato per pesare la selezione di parent di una nuova offspring,
         il valore di fittness deve essere positivo e perciò è stato bounded a [0.0001.., Inf]
         -> Fittness : (  SUM (- duals [i] * P[i] ) )
         -> Il -1 gestisce il problema di bouding
         ( Ho testato anche i logaritmi ma con scarsi risultati)
         TO DO: usare tecniche di normalizzazione
    '''
    def evaluate_fitness(self, chromosome):

        total_length = sum(chromosome[k] * self.itemLengths[k] for k in range(len(chromosome)))

        # Check if the pattern exceeds the maximum resource usage
        if total_length > self.maxValue:
            return  0.0001

        # Calculate the fitness score using the dual values
        fitness =  (-sum( -self.duals[i] * chromosome[i]  for i in range(len(self.duals))))
        
        return fitness if fitness>0 else 0.0001


    '''
        Esegue il crossover tra 'geni' per creare un individuo figlio
    '''
    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            offspring = parent1[:crossover_point] + parent2[crossover_point:]
            return offspring

        # return one of the parents as the offspring otherwise
        return random.choice([parent1, parent2])
    
    '''
        Esegue la mutazione cambiando casualmente alcuni geni nel cromosoma.
        Nota: ottenevo scarsi risultati e quindi ho deciso di rilanciare la 
        generate_first_fit_pattern
    '''
    def mutate(self, chromosome):
        # for i in range(len(chromosome)):
        #     if random.random() < self.mutation_rate:
        #         chromosome[i] = random.randint(0, self.maxValue)
        pattern = self.generate_first_fit_pattern()
        for i in range(len(chromosome)):
            chromosome[i] = pattern[i]

    '''
        Esegue l'algoritmo genetico per un numero specificato di generazioni, valutando la fitness della popolazione    corrente, creando una nuova popolazione attraverso crossover ed elitismo, generando nuovi individui offspring e sostituendo la popolazione corrente con la nuova popolazione.
    '''
    def generatePattern(self):
        self.initialize_population()
        for _ in range(self.generations):
            # Evaluate fitness for each individual in the population
            fitness_scores = [self.evaluate_fitness(chromosome) for chromosome in self.population]

            # Create a new population for the next generation
            new_population = []

            # Apply elitism - preserve the best individual in the current population
            best_index = fitness_scores.index(max(fitness_scores))
            best_chromosome = self.population[best_index]
            new_population.append(best_chromosome)

            # Generate offspring for the remaining population slots
            while len(new_population) < self.population_size:
                # Select parents for crossover
                # The selection is weighted by the fittness_scores
                parents = random.choices(self.population, weights=fitness_scores, k=2)

                # Create offspring through crossover
                offspring = self.crossover(parents[0], parents[1])

                # Mutate the offspring
                self.mutate(offspring)

                # Add the offspring to the new population
                new_population.append(offspring)

            # Replace the current population with the new population
            self.population = new_population

    '''
        Restituisce il miglior pattern di taglio ottenuto dall'ultima generazione della popolazione.
    '''
    def returnPattern(self):
        # Find the best solution from the final population
        best_fitness = float('-inf')
        best_chromosome = None

        for chromosome in self.population:
            fitness = self.evaluate_fitness(chromosome)
            if fitness > best_fitness:
                best_fitness = fitness
                best_chromosome= chromosome
        
        return best_chromosome if(best_fitness>1) else None
        
def test():
    algo = GeneticAlgorithm()
    algo.setInitData([1.0, 0.5, 0.2],[17, 21, 12], 60  )
    # min z = - 1_ S0 - 1_ S1 -1_ S2   -> 
    # K: 17 SO + 21 S1 + 12 S2 < 25
    # S0,S1,S2  >=0

    algo.run_genetic_algorithm()
    print(f'best pattern {algo.returnPattern()}')

