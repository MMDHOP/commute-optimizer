"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, random_state
import random

class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Hill Climbing optimization.

        Guidelines:
        - Search through the neighborhood greedily for candidates that minimize total travel time.
        - Handle flat local maxima / shoulders by allowing up to `max_sideways` non-improving steps.
        - Apply up to `max_restarts` to explore different starting basins.
        - Track the best objective cost seen at each major step in self.history.

        Prohibited:
        - Looping indefinitely on flat plateaus.
        """
        # TODO: Implement Hill Climbing with sideways moves and restarts
        best_state = None
        best_cost = float("inf")

        for restart in range(self.max_restarts + 1):
            if restart == 0:
                current = self.problem.generate_initial_state()
            else:
                current = random_state(self.problem)
            current_cost = self.problem.evaluate(current)
            visited = {current}
            sideways = 0

            if current_cost < best_cost:
                best_state, best_cost = current, current_cost
            self.history.append(best_cost)

            while True:
                scored = [(self.problem.evaluate(n), n) for n in get_neighbors(current, self.problem)]
                lowest = min(cost for cost, _ in scored)
                candidates = [n for cost, n in scored if abs(cost - lowest) < 1e-9]

                if lowest < current_cost - 1e-9:
                    current = random.choice(candidates)
                    sideways = 0
                elif abs(lowest - current_cost) < 1e-9 and sideways < self.max_sideways:
                    fresh = [n for n in candidates if n not in visited]
                    if not fresh:
                        break
                    current = random.choice(fresh)
                    sideways += 1
                else:
                    break

                visited.add(current)
                current_cost = lowest
                if current_cost < best_cost:
                    best_state, best_cost = current, current_cost
                self.history.append(best_cost)

        return best_state, best_cost
