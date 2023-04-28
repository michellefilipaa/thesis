from pyariadne import *
from DifferentialGame import DifferentialGame
from GlobalSearch import GlobalSearch


class main:

    def __init__(self):
        x = RealVariable("x")  # player 1
        y = RealVariable("y")  # player 2

        self.payoffs = make_function([x, y], [(x-2)*(x-3)*(x-4), y**3 - 4*(y**2) + 3*y - 1])
        game = DifferentialGame()
        roots = game.find_roots(IntervalNewtonSolver(game.tolerance, game.max_steps), self.payoffs, -10, 10)

        """
        print("Roots by Interval Newton:")
        [print(self.payoffs(root)) for root in roots]
        print("Local Maxima: ", game.test_local_max(self.payoffs, roots))
        print()

        roots2 = game.find_roots(KrawczykSolver(game.tolerance, game.max_steps), self.payoffs, -10, 10)
        print("Roots by Krawczyk:")
        [print(self.payoffs(r)) for r in roots2]
        print("Local Maxima: ", game.test_local_max(self.payoffs, roots2))
        """

        nash = GlobalSearch(self.payoffs)
        p = nash.initial_population(10)
        children = nash.crossover(p[0], p[1])
        fitness = nash.fitness(children[0])
        selection = nash.selection(p)
        print(nash.evolution(p))


if __name__ == "__main__":
    main()
