import ast as _ast
import arboles
from algoritmo import GeneticAlgorithm
import matplotlib.pyplot as plt


def fitness_fun(tree, target):
    return abs(tree.eval() - target)


def fitness_fun_penalty_deep(tree, target):
    return abs(tree.eval() - target) + tree.size()

def fitness_fun_penalty_repetition(tree, target):
    terminals = []
    counter = 0
    def countRepeated(node, terminals, repeated):
        if node.__class__ == arboles.TerminalNode:
            terminals.append(node.eval())

        for arg in node.arguments:
            if arg.__class__ == arboles.TerminalNode:
                if arg.eval() not in terminals:
                    terminals.append(arg.eval())
                else:
                    repeated += 1
            else:
                repeated, terminals = countRepeated(arg, terminals, repeated)
        return repeated, terminals
    repeated, terminals = countRepeated(tree, terminals, counter)
    return abs(tree.eval() - target) + repeated


POPULATION_SIZE = 10
MUTATION_RATE = 0.3
TARGET = 65346
TERMINALS = [25, 7, 8, 100, 4, 2]
FUNCTIONS = [arboles.AddNode, arboles.SubNode, arboles.MultNode, arboles.MaxNode]
GENERATOR = _ast.AST(FUNCTIONS, TERMINALS)
'''
print("==============================")
print("Number finder without penalty")
print("==============================")
ga = GeneticAlgorithm(POPULATION_SIZE, fitness_fun, MUTATION_RATE,
                      GENERATOR, TARGET, limit=500)
ga.run()
'''

FUNCTIONS = [arboles.AddNode, arboles.SubNode, arboles.MultNode] 
GENERATOR = _ast.AST(FUNCTIONS, TERMINALS)

'''
print("==============================")
print("Number finder with penalty for deep trees")
print("==============================")
ga = GeneticAlgorithm(POPULATION_SIZE, fitness_fun_penalty_deep, MUTATION_RATE,
                      GENERATOR, TARGET, max_deep=5, limit=500)
ga.run()
'''

'''
print("==============================")
print("Number finder with penalty for repeating terminals")
print("==============================")
ga = GeneticAlgorithm(POPULATION_SIZE, fitness_fun_penalty_repetition, MUTATION_RATE,
                      GENERATOR, TARGET)
ga.run()
print("==============================")
'''



# %% Plot max fitness by generation
'''
bests = [gen.best for gen in ga.generations]
x_axis_values = [gen.n for gen in ga.generations]

fig, ax = plt.subplots()
ax.plot(x_axis_values, bests, 'g', label='Best')
ax.set(xlabel="Number of generation", ylabel="Fitness")
ax.legend()
fig.set_size_inches(10, 8)
plt.show()
'''

# %% Plot heatmat
POPULATION_SIZE_ARRAY = [i for i in range(50, 1050, 50)]
MUTATION_RATE_ARRAY = [i / 10.0 for i in range(0, 110, 10)]

matrix = []
for mr in MUTATION_RATE_ARRAY:
    row = []
    for ps in POPULATION_SIZE_ARRAY:
        ga = GeneticAlgorithm(ps, fitness_fun_penalty_deep, mr, GENERATOR, TARGET, max_deep=5, limit=100)
        ga.run()
        measure = len(ga.generations)
        row.append(measure)
    matrix.append(row)



plt.imshow(matrix, cmap='hot')
plt.colorbar()
ax.set(xlabel='Population Size', ylabel='Mutation Ratio')
plt.show()
