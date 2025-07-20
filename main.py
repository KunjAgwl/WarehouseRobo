import pygame
import time
import sys
import random

# Warehouse parameters
GRID_SIZE = 15  # 15x15 grid
CELL_SIZE = 40  # Pixel size for each cell
DEPOT = (0, 0)  # Starting point
TASKS = [  # Sample tasks: ((pick_x, pick_y), (drop_x, drop_y))
    ((5, 1), (8, 9)),
    ((7, 4), (1, 11)),
    ((3, 6), (12, 2)),
    ((9, 5), (4, 13)),
    ((11, 8), (6, 0)),
    ((8, 2), (0, 14)),
    ((2, 9), (10, 12)),
    ((4, 10), (13, 7)),
]
NUM_TASKS = len(TASKS)
NUM_GENERATIONS = 50
POP_SIZE = 100
NUM_PARENTS = 50
MUTATION_PROB = 0.3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Warehouse Robot GA Simulation (Basic Implementation)")
clock = pygame.time.Clock()

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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

def fitness(chromosome):
    dist = calculate_route_distance(chromosome)
    return 1.0 / (1 + dist)  # Higher fitness for lower distance

def generate_initial_population():
    population = []
    for _ in range(POP_SIZE):
        chromosome = list(range(NUM_TASKS))
        random.shuffle(chromosome)
        population.append(chromosome)
    return population

def select_parents(population):
    # Tournament selection: pick 2 random, choose the better one, repeat for NUM_PARENTS
    parents = []
    for _ in range(NUM_PARENTS):
        candidates = random.sample(population, 2)
        parents.append(max(candidates, key=fitness))
    return parents

def crossover(parent1, parent2):
    # Single-point crossover, ensuring unique genes
    point = random.randint(1, NUM_TASKS - 2)
    child1 = parent1[:point] + [g for g in parent2 if g not in parent1[:point]]
    child2 = parent2[:point] + [g for g in parent1 if g not in parent2[:point]]
    return child1, child2

def mutate(chromosome):
    if random.random() < MUTATION_PROB:
        i, j = random.sample(range(NUM_TASKS), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

def evolve_population(population):
    sorted_pop = get_top_unique_chromosomes(population, num_top=5)  # Sort by fitness descending
    next_pop = sorted_pop[:5]  # Keep top 5 for elitism
    parents = select_parents(population)
    while len(next_pop) < POP_SIZE:
        p1, p2 = random.sample(parents, 2)
        child1, child2 = crossover(p1, p2)
        next_pop.append(mutate(child1))
        if len(next_pop) < POP_SIZE:
            next_pop.append(mutate(child2))
    for _ in range(5):#Random Immigrants
        new_chrom = list(range(NUM_TASKS))
        random.shuffle(new_chrom)
        next_pop[random.randint(0, POP_SIZE - 1)] = new_chrom 
    return next_pop


def get_top_unique_chromosomes(population, num_top=5):
    # Sort by fitness descending
    sorted_pop = sorted(population, key=fitness, reverse=True)
    unique_chroms = []
    seen = set()
    for chrom in sorted_pop:
        chrom_tuple = tuple(chrom)  # For uniqueness check
        if chrom_tuple not in seen:
            seen.add(chrom_tuple)
            unique_chroms.append(chrom)
            if len(unique_chroms) == num_top:
                break
    return unique_chroms



def manhattan_path(start, end):
    path = []
    current = list(start)
    while current != list(end):
        if current[0] < end[0]:
            current[0] += 1
        elif current[0] > end[0]:
            current[0] -= 1
        elif current[1] < end[1]:
            current[1] += 1
        elif current[1] > end[1]:
            current[1] -= 1
        path.append(tuple(current))
    return path

def generate_route(chromosome):
    route = [DEPOT]
    pos = DEPOT
    for gene in chromosome:
        pick, drop = TASKS[gene]
        route.extend(manhattan_path(pos, pick)[1:])
        pos = pick
        route.extend(manhattan_path(pos, drop)[1:])
        pos = drop
    return route

def draw_grid():
    screen.fill(WHITE)
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_SIZE))
    for y in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (SCREEN_SIZE, y * CELL_SIZE))

def draw_tasks():
    for pick, drop in TASKS:
        pygame.draw.circle(screen, GREEN, (pick[0] * CELL_SIZE + CELL_SIZE // 2, pick[1] * CELL_SIZE + CELL_SIZE // 2), 10)
        pygame.draw.circle(screen, RED, (drop[0] * CELL_SIZE + CELL_SIZE // 2, drop[1] * CELL_SIZE + CELL_SIZE // 2), 10)

def draw_route(route):
    for i in range(len(route) - 1):
        start = (route[i][0] * CELL_SIZE + CELL_SIZE // 2, route[i][1] * CELL_SIZE + CELL_SIZE // 2)
        end = (route[i + 1][0] * CELL_SIZE + CELL_SIZE // 2, route[i + 1][1] * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.line(screen, BLUE, start, end, 3)

def animate_robot(route):
    for pos in route:
        draw_grid()
        draw_tasks()
        draw_route(route)
        pygame.draw.circle(screen, BLUE, (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), 15)
        pygame.display.flip()
        time.sleep(0.01)  # Faster animation for GA

# Main GA loop
population = generate_initial_population()
generation = 0
running = True
while running and generation < NUM_GENERATIONS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Evolve
    population = evolve_population(population)
    best_chromosome = max(population, key=fitness)
    best_dist = calculate_route_distance(best_chromosome)
    print(f"Generation {generation + 1}: Best Distance = {best_dist}")

    # Visualize best route
    best_route = generate_route(best_chromosome)
    animate_robot(best_route)

    clock.tick(10)  # Control frame rate
    generation += 1

pygame.quit()
sys.exit()
