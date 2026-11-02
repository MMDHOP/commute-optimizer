"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


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
        current = self.problem.generate_initial_state()
        current_cost = self.problem.evaluate(current)
        self.history.append(current_cost)

        while True:
            best = min(get_neighbors(current, self.problem), key=self.problem.evaluate)
            best_cost = self.problem.evaluate(best)
            if best_cost >= current_cost:
                break
            current, current_cost = best, best_cost
            self.history.append(current_cost)

        return current, current_cost
