import ast
import arboles as t
from algoritmo import GeneticAlgorithm
import matplotlib.pyplot as plt


def fitness_fun_single_var(tree, target, var, points):
    total = 0
    for point in points:
        total += abs(tree.eval({var: point}) - target.eval({var: point}))
    return total

def fitness_fun_single_var_div(tree, target, var, points):
    total = 0
    for point in points:
        res = tree.eval({var: point})
        if res == "ERROR":
            return -1 
        total += abs(tree.eval({var: point}) - target.eval({var: point}))
    return total

POPULATION_SIZE = 10
MUTATION_RATE = 0.3
TARGET = t.SubNode(t.AddNode(t.MultNode(t.TerminalNode("x"), t.TerminalNode("x")), t.TerminalNode("x")), t.TerminalNode(6))
TERMINALS = [int(i) for i in range(-10, 11)] + ["x"]
FUNCTIONS = [t.AddNode, t.SubNode, t.MultNode]
GENERATOR = ast.AST(FUNCTIONS, TERMINALS)
print("=============================")
print("Symbolic Regression")
print("==============================")
#ga = GeneticAlgorithm(POPULATION_SIZE, fitness_fun_single_var, MUTATION_RATE,
#                      GENERATOR, TARGET, var="x", points=[i for i in range(-100, 101)])
#ga.run()
print("==============================")
print("=============================")
print("Symbolic Regression with division")
print("==============================")
FUNCTIONS = [t.AddNode, t.SubNode, t.MultNode, t.DivNode]
GENERATOR = ast.AST(FUNCTIONS, TERMINALS)
ga = GeneticAlgorithm(POPULATION_SIZE, fitness_fun_single_var_div, MUTATION_RATE,
                      GENERATOR, TARGET, var="x", points=[i for i in range(-100, 101)])
ga.run()
print("==============================")




# %% Plot max fitness by generation
bests = [gen.best for gen in ga.generations]
x_axis_values = [gen.n for gen in ga.generations]

fig, ax = plt.subplots()
ax.plot(x_axis_values, bests, 'g', label='Best')
ax.set(xlabel="Number of generation", ylabel="Fitness")
ax.legend()
fig.set_size_inches(10, 8)
plt.show()
