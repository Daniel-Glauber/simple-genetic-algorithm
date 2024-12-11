# Author: Daniel Glauber
# File: population.py
# Description: This file contains the class that represents the entire population of individual solutions.
import copy
import random
import logging
from operator import attrgetter
from individual import Individual
import settings_loader as sl

logging.basicConfig(level=logging.INFO, format='%(message)s')


class Population:
    """
    Represents the entire population of individual solutions.
    """
    def __init__(self):
        """
        Initialize the Population with settings and empty generations.
        """
        self._fitness_function = sl.get_setting("fitnessFunction")
        self._current_generation = []
        self._next_generation = []

    @property
    def current_generation(self):
        return self._current_generation

    @current_generation.setter
    def current_generation(self, value):
        self._current_generation = value

    @property
    def next_generation(self):
        return self._next_generation

    @next_generation.setter
    def next_generation(self, value):
        self._next_generation = value

    @property
    def fitness_function(self):
        return self._fitness_function

    @fitness_function.setter
    def fitness_function(self, value):
        self._fitness_function = value

    @property
    def string_size(self):
        return self._string_size

    @string_size.setter
    def string_size(self, value):
        self._string_size = value

    @property
    def population_size(self):
        return self._population_size

    @population_size.setter
    def population_size(self, value):
        self._population_size = value

    @property
    def selection_method(self):
        return self._selection_method

    @selection_method.setter
    def selection_method(self, value):
        self._selection_method = value

    @property
    def prob_apply_crossover(self):
        return self._prob_apply_crossover

    @prob_apply_crossover.setter
    def prob_apply_crossover(self, value):
        self._prob_apply_crossover = value

    @property
    def prob_apply_mutation(self):
        return self._prob_apply_mutation

    @prob_apply_mutation.setter
    def prob_apply_mutation(self, value):
        self._prob_apply_mutation = value

    @property
    def tournament_selection_size(self):
        return self._tournament_selection_size

    @tournament_selection_size.setter
    def tournament_selection_size(self, value):
        self._tournament_selection_size = value

    @property
    def failures_before_termination(self):
        return self._failures_before_termination

    @failures_before_termination.setter
    def failures_before_termination(self, value):
        self._failures_before_termination = value

    @property
    def full_debug(self):
        return self._full_debug

    @full_debug.setter
    def full_debug(self, value):
        self._full_debug = value

    @property
    def limited_debug(self):
        return self._limited_debug

    @limited_debug.setter
    def limited_debug(self, value):
        self._limited_debug = value

    def initialize_random_individual(self, string_size):
        """
        Initialize a random individual with a given string size.
        
        Args:
            string_size (int): The size of the individual's solution string.
        
        Returns:
            Individual: A new individual with a random solution.
        """
        # Create a random binary solution of the given size
        starting_solution = [random.randint(0, 1) for i in range(string_size)]
        return Individual(self._fitness_function, starting_solution)

    def initialize_random_starting_population(self):
        """
        Initialize the starting population with random individuals.
        """
        # Set the random seed for reproducibility
        random.seed(sl.get_setting("randSeed"))
        # Load settings from the settings loader
        self._full_debug = sl.get_setting("fullDebug")
        self._limited_debug = sl.get_setting("limitedDebug")
        self._string_size = sl.get_setting("stringSizeN")
        self._population_size = sl.get_setting("populationSizeN")
        self._selection_method = sl.get_setting("selectionMethod")
        self._prob_apply_crossover = sl.get_setting("probApplyCrossover")
        self._prob_apply_mutation = sl.get_setting("probApplyMutation")
        self._tournament_selection_size = sl.get_setting("tournamentSizeK")
        self._failures_before_termination = sl.get_setting("failuresBeforeTermination")
        # Initialize the current generation with random individuals
        self._current_generation = [
            self.initialize_random_individual(self._string_size) for i in range(self._population_size)
        ]
        # Log the initial population if debugging is enabled
        if self._full_debug or self._limited_debug:
            logging.debug("Initial Population")
            temp_population = copy.deepcopy(self._current_generation)
            for i in temp_population:
                logging.debug(f"{i.solution_as_string()}")

    def get_average_fitness(self):
        """
        Calculate and return the average fitness of the current generation.
        
        Returns:
            float: The average fitness of the current generation.
        """
        # Calculate the average fitness of the current generation
        self._current_average_fitness = (
            sum(individual.get_solution_fitness() for individual in self._current_generation) /
            sl.get_setting("populationSizeN")
        )
        return self._current_average_fitness

    def get_worst_fitness(self):
        """
        Get the worst fitness in the current generation.
        
        Returns:
            dict: A dictionary containing the worst fitness, solution, and index.
        """
        # Find the individual with the worst fitness
        worst_individual = min(self._current_generation, key=attrgetter('_solution_fitness'))
        worst_index = self._current_generation.index(worst_individual)
        worst_data = {
            "fitness": worst_individual.get_solution_fitness(),
            "solution": worst_individual.get_solution(),
            "index": worst_index
        }
        return worst_data

    def get_best_fitness(self):
        """
        Get the best fitness in the current generation.
        
        Returns:
            dict: A dictionary containing the best fitness, solution, and index.
        """
        # Find the individual with the best fitness
        best_individual = max(self._current_generation, key=attrgetter('_solution_fitness'))
        best_index = self._current_generation.index(best_individual)
        best_data = {
            "fitness": best_individual.get_solution_fitness(),
            "solution": best_individual.get_solution(),
            "index": best_index
        }
        return best_data

    def single_tournament_selection(self):
        """
        Perform a single tournament selection to choose parents.
        
        Returns:
            tuple: A tuple containing two selected parents.
        """
        # Select two parents using tournament selection
        return self.single_parent_selection(), self.single_parent_selection()

    def single_parent_selection(self):
        """
        Perform a single parent selection using tournament selection.
        
        Returns:
            Individual: The selected parent.
        """
        # Randomly select individuals for the tournament
        selection = random.choices(self._current_generation, k=self._tournament_selection_size)
        # Choose the best individual from the tournament
        best_parent = max(selection, key=attrgetter('_solution_fitness'))
        # Log the selection process if full debugging is enabled
        if self._full_debug:
            logging.debug("Selecting parent")
            logging.debug('\n'.join([
                f"{parent.solution_as_string()}, Fitness: {parent.get_solution_fitness()}"
                for parent in selection
            ]))
            logging.debug(f"Selected parent: {best_parent.solution_as_string()}\n")
        return best_parent

    def tournament_selection(self, empty):
        """
        Perform tournament selection and crossover to produce children.
        
        Args:
            empty: Placeholder argument.
        
        Returns:
            list: A list of children produced from the selected parents.
        """
        # Select parents and perform crossover to produce children
        parents_tuple = self.single_tournament_selection()
        children = self.uniform_crossover(parents_tuple)
        # Attempt to mutate each child
        [self.attempt_mutation(child) for child in children]
        return children

    def attempt_mutation(self, child):
        """
        Attempt to mutate a child's solution.
        
        Args:
            child (Individual): The child to mutate.
        """
        # Mutate the child with a certain probability
        if random.random() < self._prob_apply_mutation:
            indexes_to_mutate_bool_list = [random.random() < 1 / self._string_size for i in range(self._string_size)]
            if self._full_debug:
                child.mutate_solution(indexes_to_mutate_bool_list, True)
            else:
                child.mutate_solution(indexes_to_mutate_bool_list)

    def uniform_crossover(self, parents_tuple):
        """
        Perform uniform crossover on a tuple of parents to produce children.
        
        Args:
            parents_tuple (tuple): A tuple containing two parent individuals.
        
        Returns:
            list: A list of two children produced from the parents.
        """
        # Get the solutions of the parents
        parents_solution_tuple = (
            parents_tuple[0].get_solution(), parents_tuple[1].get_solution()
        )
        # Log the parents' solutions before crossover if full debugging is enabled
        if self._full_debug:
            logging.debug("Before Crossover")
            logging.debug(f"p1: {parents_tuple[0].solution_as_string()}")
            logging.debug(f"p2: {parents_tuple[1].solution_as_string()}")

        # Perform crossover with a certain probability
        if random.random() < self._prob_apply_crossover:
            # Create children by combining parents' solutions
            res = [(i, i ^ 1) for i in (random.choice([0, 1]) for i in range(self._string_size))]
            child_a = [parents_solution_tuple[parent[0]][index] for index, parent in enumerate(res)]
            child_b = [parents_solution_tuple[parent[1]][index] for index, parent in enumerate(res)]
            children = [
                Individual(self._fitness_function, child_a),
                Individual(self._fitness_function, child_b)
            ]
            # Log the children's solutions after crossover if full debugging is enabled
            if self._full_debug:
                logging.debug("After Crossover")
                logging.debug(f"c1: {children[0].solution_as_string()}")
                logging.debug(f"c2: {children[1].solution_as_string()}\n")
            return children
        else:
            # If no crossover, children are clones of parents
            children = [
                Individual(self._fitness_function, parents_tuple[0].get_solution(), parents_tuple[0].get_solution_fitness()),
                Individual(self._fitness_function, parents_tuple[1].get_solution(), parents_tuple[1].get_solution_fitness())
            ]
            # Log the children's solutions after crossover if full debugging is enabled
            if self._full_debug:
                logging.debug("After Crossover")
                logging.debug(f"c1: {children[0].solution_as_string()}")
                logging.debug(f"c2: {children[1].solution_as_string()}\n")
            return children

    def replace_current_population(self):
        """
        Replace the current generation with the next generation.
        """
        # Clear the current generation and replace it with the next generation
        self._current_generation = []
        self._current_generation = copy.deepcopy(self._next_generation)
        self._next_generation = []

    def select_mating_parents(self):
        """
        Select mating parents and produce offspring for the next generation.
        """
        # Get the best individual from the current generation
        best_individual_data = self.get_best_fitness()
        best_individual = Individual(
            self._fitness_function,
            best_individual_data["solution"],
            best_individual_data["fitness"]
        )
        # Perform selection and crossover to produce new offspring
        if self._selection_method == 0:
            new_offspring = map(self.tournament_selection, range(self._population_size // 2))
            for items in new_offspring:
                for child in items:
                    if len(self._next_generation) < self._population_size - 1:
                        self._next_generation.append(child)
            # Ensure the best individual is included in the next generation
            self._next_generation.append(best_individual)

    def get_current_generation(self):
        """
        Get a copy of the current generation.
        
        Returns:
            list: A copy of the current generation.
        """
        return self._current_generation.copy()

    def set_current_generation(self, new_generation):
        """
        Set the current generation to a new generation.
        
        Args:
            new_generation (list): The new generation to set.
        """
        self._current_generation = new_generation.copy()

    def get_next_generation(self):
        """
        Get a copy of the next generation.
        
        Returns:
            list: A copy of the next generation.
        """
        return self._next_generation.copy()

    def set_next_generation(self, new_generation):
        """
        Set the next generation to a new generation.
        
        Args:
            new_generation (list): The new generation to set.
        """
        self._next_generation = new_generation.copy()

    def get_fitness_function(self):
        """
        Get the fitness function value.
        
        Returns:
            int: The fitness function value.
        """
        return self._fitness_function

    def set_fitness_function(self, new_fitness_function):
        """
        Set a new fitness function value.
        
        Args:
            new_fitness_function (int): The new fitness function value.
        """
        self._fitness_function = new_fitness_function
