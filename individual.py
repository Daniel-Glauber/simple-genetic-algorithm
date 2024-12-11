# Author: Daniel Glauber
# File: individual.py
# Description: This file contains the class that represents an individual solution in the population.

# Class Individual represents a single solution in population
class Individual:
    """
    Represents a single solution in the population.
    """
    def __init__(self, fitness_function, starting_solution=None, solution_fitness=None):
        """
        Initialize an Individual with a fitness function and starting solution.
        
        Args:
            fitness_function (int): The fitness function value.
            starting_solution (list, optional): The starting solution as a list of integers.
            solution_fitness (int, optional): The precomputed fitness of the solution.
        """
        if starting_solution is None:
            starting_solution = []
        self._fitness_function_value = fitness_function
        self._solution = starting_solution.copy()
        self._fitness_evaluated = False
        self._solution_fitness = None
        if self._solution:
            self.evaluate_solution_fitness(solution_fitness)

    @property
    def fitness_function_value(self):
        return self._fitness_function_value

    @fitness_function_value.setter
    def fitness_function_value(self, value):
        self._fitness_function_value = value
        self._fitness_evaluated = False
        self._solution_fitness = None

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, value):
        self._solution = value
        self._fitness_evaluated = False
        self._solution_fitness = None

    @property
    def fitness_evaluated(self):
        return self._fitness_evaluated

    @fitness_evaluated.setter
    def fitness_evaluated(self, value):
        self._fitness_evaluated = value

    @property
    def solution_fitness(self):
        return self._solution_fitness

    @solution_fitness.setter
    def solution_fitness(self, value):
        self._solution_fitness = value

    def solution_as_string(self):
        """
        Get the solution as a comma-separated string.
        
        Returns:
            str: The solution as a string.
        """
        return ",".join([str(x) for x in self._solution])

    def mutate_solution(self, indexes_to_mutate_bool_list, full_debug=False):
        """
        Mutate the solution based on a list of boolean values indicating mutation points.
        
        Args:
            indexes_to_mutate_bool_list (list): A list of boolean values indicating mutation points.
            full_debug (bool, optional): Whether to print debug information.
        """
        if any(indexes_to_mutate_bool_list):
            if full_debug:
                print(f"Before Mutation: {self.solution_as_string()}")
            for index, mutate_boolean in enumerate(indexes_to_mutate_bool_list):
                if mutate_boolean:
                    # Flip the bit at the current index
                    self._solution[index] = self._solution[index] ^ 1
            # Recalculate the fitness after mutation
            self._solution_fitness = sum(self._solution)
            if full_debug:
                print(f"After Mutation: {self.solution_as_string()}\n")

    def evaluate_solution_fitness(self, solution_fitness=None):
        """
        Evaluate the fitness of the solution.
        
        Args:
            solution_fitness (int, optional): The precomputed fitness of the solution.
        """
        if solution_fitness is not None:
            self._solution_fitness = solution_fitness
        else:
            if self._fitness_function_value == 0:
                # Calculate fitness as the sum of the solution elements
                self._solution_fitness = sum(self._solution)
                self._fitness_evaluated = True

    def get_solution_fitness(self):
        """
        Get the fitness of the solution.
        
        Returns:
            int: The fitness of the solution.
        """
        if self._fitness_evaluated:
            return self._solution_fitness
        else:
            self.evaluate_solution_fitness()
            return self._solution_fitness

    def get_solution(self):
        """
        Get a copy of the solution.
        
        Returns:
            list: A copy of the solution.
        """
        return self._solution.copy()

    def set_solution(self, new_solution):
        """
        Set a new solution.
        
        Args:
            new_solution (list): The new solution to set.
        """
        self._solution = new_solution.copy()
        self._fitness_evaluated = False
        self._solution_fitness = None

    def get_fitness_function_value(self):
        """
        Get the fitness function value.
        
        Returns:
            int: The fitness function value.
        """
        return self._fitness_function_value

    def set_fitness_function_value(self, new_fitness_function_value):
        """
        Set a new fitness function value.
        
        Args:
            new_fitness_function_value (int): The new fitness function value.
        """
        self._fitness_function_value = new_fitness_function_value
        self._fitness_evaluated = False
        self._solution_fitness = None