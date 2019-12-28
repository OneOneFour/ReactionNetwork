from functools import reduce
import numpy as np
from scipy.integrate import odeint


class Reaction:
    """
    Representation of a single reaction
    """

    class ReactionDict(dict):
        def __getitem__(self, item):
            try:
                return super().__getitem__(item)
            except KeyError:
                return 0

        def flatten(self, vars):
            return np.array([self[v] for v in vars])

    @staticmethod
    def reaction_from_string(string, **kwargs):
        import re
        reduced_str = str.replace(" ", "")
        reactants_str = reduced_str.split("=")[0]
        products_str = reduced_str.split(">")[1]
        key = re.search(r"(?<=\()\w(?=\))", string)[0]
        try:
            rate = float(key)
        except ValueError:
            rate = kwargs[key]

    def __init__(self, reactants, products, rate_coefficent=1.):
        self.reactants = self.ReactionDict(reactants)
        self.products = self.ReactionDict(products)
        self.variables = {*reactants, *products}  # Get set of variables in the eqn
        self.rate_coefficent = rate_coefficent

    def __str__(self):
        return "+".join(f"{v}{k}" for k, v in self.reactants.items()) + f" =({self.rate_coefficent})> " + "+".join(
            f"{v}{k}" for k, v in self.products.items())

    def w(self, **x):
        w = self.rate_coefficent
        for x_i in self.variables:
            w *= x[x_i] ** (self.reactants[x_i])
        return w

    def w_r(self, vars):
        """
        Returns w as a scalar function f on population vector v
        """
        return lambda x: self.rate_coefficent * reduce(lambda i, j: i * j, x ** self.reactants.flatten(vars))

    def s_i(self, var):
        return self.products[var] - self.reactants[var]


class ReactionNetwork:
    """
    Group of individual reactions grouped into a linear algebra problem
    """

    def __init__(self, *reactions):
        self.reactions = reactions

        # Variables is now an ORDERED list of all variables -> represents order for vectorized calculations
        self.variables = list(reduce(lambda x, y: x | y, [r.variables for r in reactions]))
        self.__w = [r.w_r(self.variables) for r in self.reactions]

    def add_reaction(self, reaction):
        self.reactions.extend(reaction)
        self.variables = list(set(self.variables + reaction.variables))
        self.__w = [r.w_r(self.variables) for r in self.reactions]

    def idx(self, var):
        if var not in self.variables:
            raise ValueError(f"\"{var}\" is not present in the reaction network")
        return self.variables.index(var)

    @property
    def stoichmetric_matrix(self):
        try:
            return self.__s
        except AttributeError:
            self.__s = np.zeros((len(self.variables), len(self.reactions)))
            for i, variable in enumerate(self.variables):
                for r, reaction in enumerate(self.reactions):
                    self.__s[i, r] = reaction.s_i(variable)
            return self.__s

    def w(self, x):
        return np.array([w_r(x) for w_r in self.__w])

    def vars_to_vec(self, vars):
        return np.array([vars[v] for v in self.variables])

    def ode(self, x, t):
        return self.stoichmetric_matrix @ self.w(x)

    def ode_var(self, var, t=0):
        return lambda x: self.stoichmetric_matrix[self.idx(var)] @ self.w(x)

    def __odeint(self, x_0, t=None, t_min=0, t_max=1):
        if t is None:
            t = np.linspace(t_min, t_max, 100)
        if isinstance(x_0, dict):
            x_0 = self.vars_to_vec(x_0)
        return t, odeint(self.ode, x_0, t)

    def solve(self, x_0, t=None, t_min=0, t_max=1, plot=False, plot_var=None):
        t, x = self.__odeint(x_0, t=t, t_min=t_min, t_max=t_max)
        if plot:
            import matplotlib.pyplot as plt
            plt.plot(t, x[:, self.idx(plot_var)])
            plt.show()

    def phase_plot(self, x_0, plot_vars, t=None, t_min=0, t_max=1):
        t, x = self.__odeint(x_0, t=t, t_min=t_min, t_max=t_max)
        import matplotlib.pyplot as plt
        plt.plot(x[:, self.idx(plot_vars[0])], x[:, self.idx(plot_vars[1])])
        plt.show()

    def phase_swatch(self, min,max):
        


if __name__ == "__main__":
    growth_y = Reaction({"X": 1, "Y": 1}, {"Y": 2, "X": 1}, )
    growth_x = Reaction({"X": 1, "Y": 1}, {"X": 2, "Y": 1}, rate_coefficent=1.1)
    death_y = Reaction({"X": 1}, {"X": 0})
    death_x = Reaction({"Y": 1}, {"Y": 0})
    network = ReactionNetwork(growth_y, death_y, growth_x, death_x)
    network.solve({"X": 1, "Y": 1}, t_min=0, t_max=1, plot=True, plot_var="X")
    network.phase_plot({"X": 0.5, "Y": 1}, t_min=0, t_max=1, plot_vars=["X", "Y"])
