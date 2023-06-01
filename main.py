import pandas as pd
from pyariadne import *
from DifferentialGame import DifferentialGame
from GlobalSearch import GlobalSearch
from IntervalEvaluation import IntervalEvaluation
from LocalConvergence import LocalConvergence


class main:

    def __init__(self):
        x = RealVariable("x")  # player 1
        y = RealVariable("y")  # player 2

        # x**3 - 3*x**2 + 1, 3*y**4 - 16*y**3 + 18*y**2 (1) -> no nash equilibrium in (-1,1)
        # -x**3 - y**3 + 3*x*y + 5, -x**2 + 4*x*y - y**2 + 8 (2) -> no nash equilibrium in (-1.25, 1)
        # -x**2 + 2*x*y - y**2, -x**3 - y**3 + 3*x*y (3) -> 1 nash equilibrium in (1.25, 1)
        # -x**2 + 2*x*y - y**2, -x**3 - y**4 + 3*x*y (4) -> 2 nash equilibrium in (1.25, 1)
        # x**2 - y - 5, y**4 + 5*x
        self.payoff_functions = make_function([x, y], [-x**2 + 2*x*y - y**2, -x**3 - y**3 + 3*x*y])
        game = DifferentialGame()
        roots = game.find_roots(IntervalNewtonSolver(game.tolerance, game.max_steps), self.payoff_functions, -1.25, 1)

        print("Roots by Interval Newton:")
        print(*roots, sep=' ')
        print()

        tester = game.test_local_max(self.payoff_functions, roots)
        print("Local Maxima: ", tester, "\n")

        """
        print("Payoffs:")
        [print(self.payoffs(root)) for root in roots]
        print()
        """

        roots2 = game.find_roots(KrawczykSolver(game.tolerance, game.max_steps), self.payoff_functions, -1.25, 1)
        print("Roots by Krawczyk:")
        print(*roots2, sep=' ')
        print()

        print("Local Maxima: ", game.test_local_max(self.payoff_functions, roots2), "\n")

        search = GlobalSearch(self.payoff_functions, -1.25, 1)

        grid, payoff_matrix = search.create_grid()
        # Nash Brute Force Method 1
        approx_nash = search.brute_force_nash_equilibrium(payoff_matrix, grid)

        print("Approximate Roots with Method 1")
        print(*approx_nash, sep=' ')
        print()

        # Nash Best Response Brute Force Method
        approx_points, exact_points = search.brute_force(payoff_matrix, grid)

        print("Approximate Roots with Best Response:")
        print(*approx_points, sep=' ')
        print()

        print("Exact Roots:")
        print(*exact_points, sep=' ')
        print()

        nash_payoffs = [self.payoff_functions(roots[i]) for i in range(len(tester)) if tester[i]]
        print("Payoffs:")
        print(*nash_payoffs, sep=' ')
        print()

        max_nash_strategies = [roots[i] for i in range(len(tester)) if tester[i]]
        max_check = LocalConvergence()

        inter = IntervalEvaluation(self.payoff_functions)
        intervals = inter.split_intervals(inter.intervals)

        print()
        for nash in exact_points:
            eval_p0 = inter.interval_evaluation(nash, inter.ari_intervals, 0)
            eval_p1 = inter.interval_evaluation(nash, inter.ari_intervals, 1)
            print("{} is a Global Max".format(nash) if all(eval_p0 and eval_p1) else "{} is not global max".format(nash))
        # max_check.nash_evaluation(self.payoff_functions, max_nash_strategies)


if __name__ == "__main__":
    main()
