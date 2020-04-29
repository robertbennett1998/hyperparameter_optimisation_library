import numpy
import random
import time
import hpo.strategies.genetic_algorithm.genetic_algorithm_crossover_stratergies as crossover_strategies
import hpo.strategies.genetic_algorithm.genetic_algorithm_selection_stratergies as survivour_selection_strategies
import hpo.strategies.genetic_algorithm.genetic_algorithm_mutation_stratergies as mutation_strategies
import hpo.strategies.genetic_algorithm.genetic_algorithm_chromosome
from hpo.hpo_results import Result
import hpo
from tqdm import tqdm
import os
import json

class GeneticAlgorithm(hpo.Strategy):
    def __init__(self, population_size, max_iterations, chromosome_type, crossover_stratergy = "onepoint", survivour_selection_stratergy = "threshold", mutation_stratergy = "percentage"):
        super().__init__()
        self._population_size = population_size
        self._population = [None for i in range(0, population_size)]

        self._max_iterations = max_iterations

        self._chromosome_type = chromosome_type

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
        total_fitness = 0
        best_fitness = 0

        number_of_failed_iterations = 0
        for chromosome in self._population.copy():
            fitness = chromosome.fitness()

            if fitness > best_fitness:
                best_fitness = fitness

            if fitness == 0.0:
                number_of_failed_iterations += 1

            total_fitness += fitness

        if not len(self._population) - number_of_failed_iterations == 0:
            info["average_population_fitness"] = total_fitness / (len(self._population) - number_of_failed_iterations)
        else:
            info["average_population_fitness"] = 0

        info["best_fitness"] = best_fitness
        return info

    def generation_history(self):
        return self._generation_history

    def execute(self, data_type, results, model_exception_handler=None):
        best_chromosome = None
        self._generation_history = list()
        self._generate_population()

        for generation in tqdm(range(0, self._max_iterations + 1), unit="generation"):
            # calculate fitnesses
            print("Running Population For Iteration %d:" % generation)
            chromosome_number = 1
            for chromosome in tqdm(self._population, unit="chromosome"):
                training_history, final_weights = chromosome.execute(data_type, model_exception_handler)
                results.add_result(Result(chromosome.model_configuration(), training_history, chromosome.fitness() if chromosome.fitness() > 0 else None, final_weights, meta_data={"Generation": generation, "Chromosome": chromosome_number}))
                chromosome_number += 1

            results.meta_data(self.population_info())

            # create offset
            offspring = self._generate_offspring()

            # mutate
            for i in range(len(offspring)):
                offspring[i] = self._mutation_stratergy.execute(offspring[i])

            best_chromosome = self._get_best_chromosome()

            # select surviors
            self._survivour_selection_stratergy.execute(self._population)

            # age population
            for chromosome in self._population:
                chromosome._age = chromosome.age() + 1

            # re-populate
            for i in range(self._population_size - len(self._population)):
                self._population.append(offspring[random.sample(range(len(offspring)), 1)[0]])

            if not self._population_size - len(self._population) == 0:
                for i in range(self._population_size - len(self._population)):
                    self._population.append(self._generate_chromosome())

        return results

    def mutation_strategy(self):
        return self._mutation_stratergy

    def crossover_strategy(self):
        return self._crossover_stratergy

    def survivour_selection_strategy(self):
        return self._survivour_selection_stratergy

    def chromosome_type(self):
        return self._chromosome_type
