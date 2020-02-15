import numpy
import random
import time
import hpo.strategies.genetic_algorithm.genetic_algorithm_crossover_stratergies as crossover_strategies
import hpo.strategies.genetic_algorithm.genetic_algorithm_selection_stratergies as survivour_selection_strategies
import hpo.strategies.genetic_algorithm.genetic_algorithm_mutation_stratergies as mutation_strategies
import hpo.strategies.genetic_algorithm.genetic_algorithm_chromosome
import hpo
from tqdm import tqdm
from datetime import datetime
import os
import json

class GeneticAlgorithm(hpo.Strategy):
    def __init__(self, population_size, max_iterations, chromosome_type, crossover_stratergy = "onepoint", survivour_selection_stratergy = "threshold", mutation_stratergy = "percentage"):
        self._population_size = population_size
        self._population = [None for i in range(0, population_size)]
        self._generation_history = list()

        self._max_iterations = max_iterations

        self._chromosome_type = chromosome_type

        timestamp = datetime.now().strftime("%d_%b_%Y__%H_%M_%S")
        self._history_file_path = os.path.join(os.getcwd(), "generation_history_%s.json" % timestamp)
        
        if isinstance(crossover_stratergy, str):
            self._crossover_stratergy = crossover_strategies.resolve_crossover_stratergy(crossover_stratergy, self._chromosome_type)
        else:
            self._crossover_stratergy = crossover_stratergy

        if isinstance(survivour_selection_stratergy, str):
            self._survivour_selection_stratergy = survivour_selection_strategies.resolve_survivour_selection_stratergy(survivour_selection_stratergy)
        else:
            self._survivour_selection_stratergy = survivour_selection_stratergy
        
        if isinstance(mutation_stratergy, str):
            self._mutation_stratergy = mutation_strategies.resolve_mutation_strategy(mutation_stratergy, chromosome_type)
        else:
            self._mutation_stratergy = mutation_stratergy
    
    def population(self):
        return self._population

    def _generate_chromosome(self, randomise=True):
        chromosome = self._chromosome_type()

        if randomise:
            for gene in chromosome.genes():
                    value_index = 0
                    values = random.sample(gene.value_range(), len(gene.value_range()))
                    gene.value(values[value_index])
                    while not chromosome.check_gene_constraints(gene):
                        value_index += 1
                        gene.value(values[value_index])
                        
        return chromosome

    def _generate_population(self):
        print("Generating Population:")
        for i in tqdm(range(0, self._population_size), unit="chromosones"):
            self._population[i] = self._generate_chromosome(i > 0)

    def _select_mating_partner(self):
        totalFitness = 0
        for chromosome in self._population:
            totalFitness += chromosome.fitness()
        
        selectedValue = random.randint(0, totalFitness)
        currentValue = 0
        for chromosome in self._population:
            currentValue += chromosome.fitness()
            if currentValue >= selectedValue:
                return chromosome

        return None

    def _generate_offspring(self):
        offspring = []

        for chromosome in self._population:
            matingPartner = self._select_mating_partner()
            offspring.append(self._crossover_stratergy.execute(chromosome, matingPartner))

        return offspring

    def _get_best_chromosome(self):
        best_chromosome = None
        best_fitness = 0
        for chromosome in self._population:
            fitness = chromosome.fitness()
            if fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = chromosome

        return best_chromosome

    def population_info(self):
        info = dict()
        fitnesses = list()
        population = list()
        total_fitness = 0
        best_fitness = 0
        best_chromosome = None

        number_of_failed_iterations = 0
        for chromosome in self._population.copy():
            fitness = chromosome.fitness()
            population.append(chromosome.decode())

            if fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = chromosome.decode()

            if fitness == 0.0:
                number_of_failed_iterations += 1

            total_fitness += fitness
            fitnesses.append(fitness)


        info["population_fitnesses"] = fitnesses
        info["population"] = population
        info["avgerage_population_fitness"] = total_fitness / (len(self._population) - number_of_failed_iterations)
        info["best_fitness"] = best_fitness
        info["best_chromosome"] = best_chromosome

        return info

    def generation_history(self):
        return self._generation_history

    def _execute_population(self, data_type, iteration=0 ):
        print("Running Population For Iteration %d:" % iteration)
        for chromosome in tqdm(self._population, unit="chromosone"):
            chromosome.execute(data_type)

        self._generation_history.append(self.population_info().copy())
        print("Outputting generation results to %s" % self._history_file_path)
        history_file = open(self._history_file_path, "w+")
        print(self._generation_history)
        history_file.write(json.dumps(self._generation_history))
        history_file.close()

    def execute(self, data_type):
        best_chromosome = None
        self._generation_history = list()
        self._generate_population()
        self._execute_population(data_type)

        for iteration in tqdm(range(1, self._max_iterations + 1), unit="generation"):
            #create offset
            offspring = self._generate_offspring()

            #mutate
            for i in range(len(offspring)):
                offspring[i] = self._mutation_stratergy.execute(offspring[i])

            best_chromosome = self._get_best_chromosome()

            #select surviors
            self._survivour_selection_stratergy.execute(self._population)

            #age population
            for chromosome in self._population:
                chromosome._age = chromosome.age() + 1

            #re-populate
            for i in range(self._population_size - len(self._population)):
                self._population.append(offspring[random.sample(range(len(offspring)), 1)[0]])

            if not self._population_size - len(self._population) == 0:
                for i in range(self._population_size - len(self._population)):
                    self._population.append(self._generate_chromosome())

            #calculate new fitnesses
            self._execute_population(data_type, iteration)
            best_chromosome = self._get_best_chromosome()

        self._population.sort(key=lambda x : x.fitness(), reverse=True)
        return self._population, best_chromosome

    def mutation_strategy(self):
        return self._mutation_stratergy

    def crossover_strategy(self):
        return self._crossover_stratergy

    def survivour_selection_strategy(self):
        return self._survivour_selection_stratergy

    def chromosome_type(self):
        return self._chromosome_type
