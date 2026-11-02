"""
algorithms/genetic_algorithm.py
Population-based optimization using selection, recombination, and mutation.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, crossover, random_state
import random

class GeneticAlgorithmSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.population_size: int = self.params.get("population_size", 30)
        self.generations: int = self.params.get("generations", 100)
        self.crossover_rate: float = self.params.get("crossover_rate", 0.8)
        self.mutation_rate: float = self.params.get("mutation_rate", 0.2)
        self.elitism: int = self.params.get("elitism", 2)
        self.tournament_size: int = self.params.get("tournament_size", 3)
        
    def solve(self) -> Tuple[State, float]:
        """
        Executes Genetic Algorithm optimization.

        Guidelines:
        - Initialize a population of valid candidate solutions.
        - Design a fitness metric suitable for minimizing commute travel time (lower cost -> higher fitness).
        - Use selection operators (such as tournament or roulette selection) to pick parents.
        - Pair parents to produce offspring via `crossover()`, and apply stochastic mutation.
        - Preserve the top candidates across generations if using elitism.
        - Track best population performance per generation in self.history.

        Encouraged:
        - Experimenting with population size, selection pressure, and operator rates to balance exploration vs. exploitation.
        """
        # TODO: Implement Genetic Algorithm
        population = [self.problem.generate_initial_state()]
        while len(population) < self.population_size:
            population.append(random_state(self.problem))

        best_state = None
        best_cost = float("inf")

        for _ in range(self.generations):
            costs = {s: self.problem.evaluate(s) for s in population}
            ranked = sorted(population, key=lambda s: costs[s])

            if costs[ranked[0]] < best_cost:
                best_state, best_cost = ranked[0], costs[ranked[0]]
            self.history.append(best_cost)

            next_population = ranked[:self.elitism]
            while len(next_population) < self.population_size:
                parent1 = self._tournament(population, costs)
                parent2 = self._tournament(population, costs)

                if random.random() < self.crossover_rate:
                    child = crossover(parent1, parent2, self.problem)
                else:
                    child = parent1

                if random.random() < self.mutation_rate:
                    child = random.choice(get_neighbors(child, self.problem))

                next_population.append(child)

            population = next_population

        return best_state, best_cost

    def _tournament(self, population, costs):
        contenders = random.sample(population, min(self.tournament_size, len(population)))
        return max(contenders, key=lambda s: 1.0 / costs[s])
