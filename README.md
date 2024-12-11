# Simple Genetic Algorithm (SGA)

## Overview

The Simple Genetic Algorithm (SGA) is a binary genetic algorithm implementation designed for solving optimization problems. It demonstrates key genetic algorithm principles such as selection, crossover, mutation, and replacement. The project aims to identify the optimal solution to a basic fitness problem called "onemax," where the goal is to maximize the sum of bits in a binary string.

## Features

- **Binary Representation**: Solutions are represented as binary strings.
- **Configurable Settings**: Settings can be adjusted via a settings file (`gasettings.dat` by default).
- **Genetic Operators**: Implements tournament selection, uniform crossover, bit-flip mutation, and elitism.
- **Debugging Modes**: Provides limited and full debugging modes for detailed analysis.

## Settings

Settings for the algorithm are configurable in a `.dat` file. Below is a list of supported settings and their effects:

| Setting                      | Description                                                                                  | Default Value |
|------------------------------|----------------------------------------------------------------------------------------------|---------------|
| `randSeed`                   | Random seed for reproducibility.                                                             | 123           |
| `populationSizeN`            | Population size for each generation.                                                         | 100           |
| `stringSizeN`                | Length of the binary strings in the population.                                              | 50            |
| `probApplyCrossover`         | Probability of applying crossover to selected parents.                                       | 0.6           |
| `probApplyMutation`          | Probability of applying mutation to offspring.                                               | 1.0           |
| `selectionMethod`            | Selection method for parents (e.g., tournament selection).                                   | 0             |
| `tournamentSizeK`            | Tournament size for parent selection.                                                        | 2             |
| `fitnessFunction`            | Fitness function to use (0 = onemax).                                                        | 0             |
| `terminateOnFailure`         | Whether to terminate if no improvement in fitness is seen for 3 generations.                 | 1             |
| `failuresBeforeTermination`  | Number of failures allowed before termination.                                               | 0             |

### Effects of Settings

- **Population Size (`populationSizeN`)**: Larger populations improve diversity but increase computational cost.
- **String Size (`stringSizeN`)**: Determines the length of the solution. Larger strings require more generations to converge.
- **Crossover and Mutation Probabilities**: Higher probabilities encourage exploration but may disrupt good solutions.
- **Tournament Size (`tournamentSizeK`)**: Larger sizes bias selection towards fitter individuals.
- **Termination Settings**: Control when the algorithm halts based on performance stagnation.

## Usage

### Running the Program

To run the program, use the following command:
```bash
python3 sga.py [-h] [-g] [-G] [settings_file]
```

Arguments:
- `-h`: Display help message and exit.
- `-g`: Enable limited debugging.
- `-G`: Enable full debugging.
- `settings_file`: Optional custom settings file (defaults to `gasettings.dat`).

### Debugging Modes

- **Limited Debugging (`-g`)**: Outputs generation statistics, including fitness values and solutions.
- **Full Debugging (`-G`)**: Provides detailed logs of genetic operations (e.g., crossover, mutation).

## Results

The algorithm successfully determined the minimum population size for various string lengths:

| String Size | Minimum Population Size |
|-------------|--------------------------|
| 20          | 7                        |
| 30          | 8                        |
| 40          | 24                       |
| 50          | 34                       |
| ...         | ...                      |
| 600         | 191                      |

**Trendline Equation**: `f(min_population_size) = 0.9806(string_size)^0.8351`  
**Accuracy**: The model's predictions are within 7% of the actual values.

## Limitations

The algorithm is memory-intensive for large string sizes due to the storage structure. For example, with a string size of 1,000,000, the required memory exceeds 430 GB using Python integers. Optimizing memory usage (e.g., using NumPy) can significantly reduce this requirement.

## License

This project is released under [The Unlicense](https://unlicense.org/). You are free to use, modify, and distribute this software without restriction.

---

For additional details, refer to the accompanying code files and experiment results.

