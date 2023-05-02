from pyariadne import *
from DifferentialGame import DifferentialGame
from GlobalSearch import GlobalSearch
from LocalConvergence import LocalConvergence


class main:

    def __init__(self):
        x = RealVariable("x")  # player 1
        y = RealVariable("y")  # player 2

        # mix the strategies
        # x**3 - 3*x**2 + 1, 3*y**4 - 16*y**3 + 18*y**2
        # -x**3 - y**3 + 3*x*y + 5, -x**2 + 4*x*y - y**2 +8
        self.payoffs = make_function([x, y], [x**3 - 3*x**2 + 1, 3*y**4 - 16*y**3 + 18*y**2])
        game = DifferentialGame()
        roots = game.find_roots(IntervalNewtonSolver(game.tolerance, game.max_steps), self.payoffs, -1, 10)

        print("Roots by Interval Newton:")
        print(*roots, sep=' ')
        print()

        tester = game.test_local_max(self.payoffs, roots)
        print("Local Maxima: ", tester)
        print()

        # print("Nash Payoff Values: ", game.payoff_at_max(self.payoffs, tester, roots))

        """
        print("Payoffs:")
        [print(self.payoffs(root)) for root in roots]
        print()

        
        
        roots2 = game.find_roots(KrawczykSolver(game.tolerance, game.max_steps), self.payoffs, -10, 10)
        print("Roots by Krawczyk:")
        [print(self.payoffs(r)) for r in roots2]
        print("Local Maxima: ", game.test_local_max(self.payoffs, roots2))
        """
        search = GlobalSearch(self.payoffs)
        grid = search.create_grid()
        matrix = search.payoff_matrix(grid)
        print(search.brute_force_nash_equilibrium(matrix))


if __name__ == "__main__":
    main()
