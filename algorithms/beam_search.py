"""
algorithms/beam_search.py
Local Beam Search maintaining K parallel candidate states.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, random_state


class LocalBeamSearchSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.beam_width: int = self.params.get("beam_width", 5)
        self.max_iterations: int = self.params.get("max_iterations", 150)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Local Beam Search.

        Guidelines:
        - Maintain a set of `beam_width` parallel configurations.
        - In each iteration, generate neighbors from all active states in the beam.
        - Pool and rank all generated successors collectively, then retain the top `beam_width` states.
        - Halt when the beam ceases to improve or reaches max_iterations.
        - Record the best cost of the population at each step in self.history.

        Encouraged:
        - Ensuring diversity across states in the beam to prevent collapse into a single redundant path.

        Prohibited:
        - Treating this as K independent, non-communicating searches.
        """
        # TODO: Implement Local Beam Search
        beam = [self.problem.generate_initial_state()]
        while len(beam) < self.beam_width:
            candidate = random_state(self.problem)
            if candidate not in beam:
                beam.append(candidate)

        best_state = min(beam, key=self.problem.evaluate)
        best_cost = self.problem.evaluate(best_state)
        self.history.append(best_cost)

        for _ in range(self.max_iterations):
            pool = set(beam)
            for state in beam:
                pool.update(get_neighbors(state, self.problem))

            ranked = sorted(pool, key=self.problem.evaluate)
            new_beam = ranked[:self.beam_width]

            if set(new_beam) == set(beam):
                break
            beam = new_beam

            top_cost = self.problem.evaluate(beam[0])
            if top_cost < best_cost:
                best_state, best_cost = beam[0], top_cost
            self.history.append(best_cost)

        return best_state, best_cost
