![Warehouse](https://github.com/user-attachments/assets/b7d36306-a5d8-4dc9-a9ac-b0f821744f37)
# Warehouse Robot Genetic Algorithm Implementation

You can check Warehouse.gif

This document explains the genetic algorithm components used to optimize warehouse robot routing for pick-and-drop tasks.
I tried implmenting genetic algorithm to optimize the path that robot takes to visit the coordinated in such a way that it minimizes manhattan distance. 

## Problem Overview

The system optimizes the order in which a robot should complete warehouse tasks. Each task consists of picking up an item from one location and dropping it at another location. The goal is to minimize the total travel distance.
The code is kinda messy coz not enough time but it kinda works.It was actually working optimizng path.

<img width="300" height="329" alt="image" src="https://github.com/user-attachments/assets/248b8b1d-3d0a-4478-ab13-a7a2478474a4" />

![Warehouse](https://github.com/user-attachments/assets/69d39371-c471-412b-85a8-c1bdb082a12d)

## Genetic Algorithm Parameters
'''python
    NUM_TASKS = len(TASKS) # Number of tasks (8 in this case)
    NUM_GENERATIONS = 50 # Number of evolution cycles
    POP_SIZE = 100 # Population size
    NUM_PARENTS = 50 # Number of parents selected for reproduction
    MUTATION_PROB = 0.3 # Probability of mutation (30%)


## Core GA Functions

### Distance Calculation

    def manhattan_distance(a, b):
      return abs(a - b) + abs(a - b)
**Purpose**: Calculates Manhattan distance between two points. This is the primary distance metric used since the robot can only move horizontally and vertically (like in a grid-based warehouse).

### Route Distance Evaluation
    def calculate_route_distance(chromosome):
      pos = DEPOT
      dist = 0
      for gene in chromosome:
      pick, drop = TASKS[gene]
      dist += manhattan_distance(pos, pick)
      pos = pick
      dist += manhattan_distance(pos, drop)
      pos = drop
      return dist

**Purpose**: Calculates the total distance for a complete route represented by a chromosome. Each gene in the chromosome represents a task index, and the function calculates the distance from current position to pickup location, then from pickup to drop location for each task in sequence.

### Fitness Function

    def fitness(chromosome):
      dist = calculate_route_distance(chromosome)
      return 1.0 / (1 + dist) # Higher fitness for lower distance


**Purpose**: Converts distance to fitness score. Uses inverse relationship so shorter distances result in higher fitness values. The `+1` prevents division by zero.

### Population Initialization
    def generate_initial_population():
      population = []
      for _ in range(POP_SIZE):
      chromosome = list(range(NUM_TASKS))
      random.shuffle(chromosome)
      population.append(chromosome)
      return population

**Purpose**: Creates initial population of random solutions. Each chromosome is a permutation of task indices (0 to NUM_TASKS-1), representing different orders of completing the tasks.

### Crossover Operation
    def crossover(parent1, parent2):
      point = random.randint(1, NUM_TASKS - 2)
      child1 = parent1[:point] + [g for g in parent2 if g not in parent1[:point]]
      child2 = parent2[:point] + [g for g in parent1 if g not in parent2[:point]]
      return child1, child2

**Purpose**: Performs **single-point crossover** while ensuring each task appears exactly once in each child. Takes genes up to the crossover point from one parent, then fills remaining positions with genes from the other parent (avoiding duplicates).

### Population Evolution
    def evolve_population(population):
      sorted_pop = get_top_unique_chromosomes(population, num_top=5)
      next_pop = sorted_pop[:5] # Keep top 5 for elitism
      parents = select_parents(population)
      while len(next_pop) < POP_SIZE:
      p1, p2 = random.sample(parents, 2)
      child1, child2 = crossover(p1, p2)
      next_pop.append(mutate(child1))
      if len(next_pop) < POP_SIZE:
      next_pop.append(mutate(child2))
      # Random immigrants
      for _ in range(5):
      new_chrom = list(range(NUM_TASKS))
      random.shuffle(new_chrom)
      next_pop[random.randint(0, POP_SIZE - 1)] = new_chrom
      return next_pop
**Purpose**: Main evolution function that creates the next generation using:
- **Elitism**: Keeps top 5 unique solutions
- **Reproduction**: Creates offspring through crossover and mutation
- **Random Immigration**: Adds 5 completely random solutions to maintain diversity
