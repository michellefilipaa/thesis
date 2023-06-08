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

        # x**3 - 3*x**2 + 1, 3*y**4 - 16*y**3 + 18*y**2  -> no nash equilibrium in (-1,1)
        # -x**3 - y**3 + 3*x*y + 5, -x**2 + 4*x*y - y**2 + 8 -> 1 nash equilibrium in (-5, 5)
        # -x**2 + 2*x*y - y**2, -x**3 - y**3 + 3*x*y (2) -> 1 nash equilibrium in (-1.25, 1)
        # -x**2 + 2*x*y - y**2, -x**3 - y**4 + 3*x*y (1) -> 2 nash equilibrium in (-1.25, 1)
        # -x**4 - y**4 + 2*(x**2) - 2*(y**2), x*y + x**2 - y**2 (3) -> 2 nash in (-1.25, 1)
        # -(x**4 + y**4) + 2*(x**2 + y**2),  x**2 - y**4 + 2*x*y -> global search doesnt work
        # -x**3 - y**3 + 3*x*y, -x**3 - y**4 + 3*x*y (4) -> 1 nash in (-1.25, 1)
        self.payoff_functions = make_function([x, y], [-x**4 - y**4 + 2*(x**2) - 2*(y**2), x*y + x**2 - y**2])
        game = DifferentialGame()
        roots = game.find_roots(IntervalNewtonSolver(game.tolerance, game.max_steps), self.payoff_functions)

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
        approx_nash, converged_nash = search.brute_force_nash_equilibrium(payoff_matrix, grid)

        print("Approximate Roots with Method 1")
        print(*approx_nash, sep=' ')
        print()

        print("Converged Roots with Method 1")
        print(*converged_nash, sep=' ')
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

        print("Best strategies for each player:")
        max_check.compare_payoffs(self.payoff_functions, max_nash_strategies, 0)
        max_check.compare_payoffs(self.payoff_functions, max_nash_strategies, 1)
        print()

        print("Determining if the Nash is a Global Nash:")
        inter = IntervalEvaluation(self.payoff_functions)
        for nash in max_nash_strategies:
            eval_p0 = inter.interval_evaluation(nash, inter.ari_intervals, 0)
            eval_p1 = inter.interval_evaluation(nash, inter.ari_intervals, 1)
            print("{} is a Global Max".format(nash) if all(eval_p0 and eval_p1) else "{} is not global max".format(nash))
        print()
        """
        print("actually not a global max")
        nash = grid[5][4]
        eval_p0 = inter.interval_evaluation(nash, inter.ari_intervals, 0)
        eval_p1 = inter.interval_evaluation(nash, inter.ari_intervals, 1)
        print("{} is a Global Max".format(nash) if all(eval_p0 and eval_p1) else "{} is not global max".format(nash))
        """


if __name__ == "__main__":
    main()
