# Author: Daniel Glauber
# File: sga.py
# Description: This file contains the controller for the simple genetic algorithm (SGA).
import sys
from population import Population
import settings_loader as sl
import time
from typing import Dict, List

# Constants
TERMINATE_ON_FAILURE = "terminateOnFailure"
FAILURES_BEFORE_TERMINATION = "failuresBeforeTermination"
STRING_SIZE_N = "stringSizeN"
FULL_DEBUG = "fullDebug"
LIMITED_DEBUG = "limitedDebug"

# This class is the controller for the simple ga algorithm
class SGAController:
    """
    Controller for the simple genetic algorithm (SGA).
    """
    def __init__(self):
        """
        Initialize the SGAController with settings and initial population.
        """
        self.saved_generation_data: List[Dict] = []
        self.population = Population()
        self.terminate_on_failure = sl.get_setting(TERMINATE_ON_FAILURE) == 1
        self.failures_remaining = sl.get_setting(FAILURES_BEFORE_TERMINATION)
        self.string_size = sl.get_setting(STRING_SIZE_N)
        self.generation_number = 1
        self.full_debug = sl.get_setting(FULL_DEBUG)
        self.limited_debug = sl.get_setting(LIMITED_DEBUG)
        self.terminate_run = False

    def get_generation_data(self) -> None:
        """
        Collect data for the current generation including best, average, and worst fitness.
        """
        self.generation_data = {}
        self.generation_data["generation"] = self.generation_number
        self.generation_data["best"] = self.population.get_best_fitness()
        self.generation_data["average"] = self.population.get_average_fitness()
        self.generation_data["worst"] = self.population.get_worst_fitness()

    def save_generation_data(self) -> bool:
        """
        Save the data for the current generation and determine if termination is needed.
        
        Returns:
            bool: True if the run needs to be terminated, False otherwise.
        """
        needs_termination = False
        self.get_generation_data()
        message_array = [
            f"Generation {self.generation_number}: ",
            f"(B: {self.generation_data['best']['fitness']},",
            f"A: {self.generation_data['average']},",
            f"W: {self.generation_data['worst']['fitness']})"
        ]
        message = ' '.join(message_array)
        self.generation_data['message'] = message
        print(message)
        
        # Debugging information if enabled
        if self.full_debug or self.limited_debug:
            debug_array = [
                "Current Population",
                '\n'.join([i.solution_as_string() for i in self.population.get_current_generation()]),
                ' '.join(["Best Solution =", ','.join([str(i) for i in self.generation_data['best']['solution']])]),
                ' '.join(["Worst Solution =", ','.join([str(i) for i in self.generation_data['worst']['solution']]), '\n'])
            ]
            print('\n'.join(debug_array))
        
        self.saved_generation_data.append(self.generation_data)

        # Check if the best fitness matches the string size, indicating success
        if self.string_size == self.generation_data['best']['fitness']:
            success_array = [
                ' '.join(["Global Best Fitness =", str(self.generation_data['best']['fitness'])]),
                ' '.join(["Global Best Solution =", ','.join([str(i) for i in self.generation_data['best']['solution']])]),
                ' '.join(["Global Best was at index", str(self.generation_data['best']['index']), "of", str(len(self.population.get_current_generation()))]),
                ' '.join(["Average Fitness:", str(self.generation_data['average'])]),
                ' '.join(["Worst Fitness:", str(self.generation_data['worst']['fitness'])]),
            ]
            print('\n'.join(success_array))
            print("SUCCESS\n")
            needs_termination = True

        if len(self.saved_generation_data) == 4:
            self.saved_generation_data.pop(0)
            oldest_gen_best = self.saved_generation_data[0]["best"]["fitness"]
            oldest_gen_average = self.saved_generation_data[0]['average']
            for index, data in enumerate(self.saved_generation_data[1:], start=1):
                if data["best"]["fitness"] >= oldest_gen_best and data['average'] > oldest_gen_average:
                    break
                elif index == 2 and data["best"]["fitness"] <= oldest_gen_best and data['average'] < oldest_gen_average:
                    if self.failures_remaining == 0:
                        needs_termination = True
                        best_generation = max(self.saved_generation_data, key=lambda x: x["best"]["fitness"])["best"]
                        worst_generation = min(self.saved_generation_data, key=lambda x: x["worst"]["fitness"])["worst"]
                        best_average = max(self.saved_generation_data, key=lambda x: x["average"])["average"]
                        worst_average = min(self.saved_generation_data, key=lambda x: x["average"])["average"]
                        failure_array = [
                            f"Best Fitness in previous 3 generations = {best_generation['fitness']}",
                            f"Best Solution in previous 3 generations = {','.join(map(str, best_generation['solution']))}",
                            f"Worst Fitness in previous 3 generations = {worst_generation['fitness']}",
                            f"Worst Solution in previous 3 generations = {','.join(map(str, worst_generation['solution']))}",
                            f"Best Average Fitness in previous 3 generations: {best_average}",
                            f"Worst Average Fitness in previous 3 generations: {worst_average}",
                        ]
                        print('\n'.join(failure_array))
                        print("FAILED\n")
                    else:
                        self.failures_remaining -= 1
                        print("Failed")
                        print(f"Failures remaining before termination {self.failures_remaining}")
        return needs_termination

    def run(self) -> None:
        """
        Execute the genetic algorithm until termination conditions are met.
        """
        try:
            terminate_run = False
            self.population.initialize_random_starting_population()
            terminate_run = self.save_generation_data()
            self.generation_number += 1
            while not terminate_run:
                self.population.select_mating_parents()
                self.population.replace_current_population()
                terminate_run = self.save_generation_data()
                self.generation_number += 1
        except (ValueError, KeyError, IndexError) as e:
            print(f"An error occurred during the run: {e}")

if __name__ == "__main__":
    """
    Main entry point for the SGA program.
    """
    try:
        start = time.time()
        sl.load_settings(sys.argv)
        sga_controller = SGAController()
        sga_controller.run()
        end = time.time()
        print(f"Execution time: {end-start} seconds")
    except (FileNotFoundError, ValueError, KeyError, IndexError) as e:
        print(f"An error occurred: {e}")
