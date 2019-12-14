# para crear copias de los arboles
from copy import deepcopy
# random
import random

# esta funcion dice si el argumento es una funcion o no


def is_function(f):
    return hasattr(f, "__call__")

# esto nos permite recorrer una lista de a pedazos
# ejemplo el input es [1,2,3,4,5,6,7,8]
# con n=2 esta funcion nos hara tener
# [(1,2), (3,4), (5,6), (7,8)]


def chunks(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]


class Node:
    def __init__(self, function):
        # nos aseguramos que el nodo recibe una funcion
        assert is_function(function)
        self.operation = function
        # esto nos permite contar cuantos argumentos recibe la funcion
        self.num_arguments = function.__code__.co_argcount
        self.arguments = []
        self.n = 0
        self.value = None

    # funcion para evaluar un nodo (calcular el resultado)
    def eval(self, dict={}):
        # es importante chequear que los argumentos que nos dieron
        # coincidan con los argumentos que necesitamos
        assert len(self.arguments) == self.num_arguments

        # verificar que no haya una division por 0
        for node in self.arguments:
            if node.eval(dict) == "ERROR":
                return "ERROR"

        # evaluamos los argumentos, y luego los pasamos como argumentos a
        # la operacion
        # NOTA: esto -> *[...] significa que separa los elementos de la lista
        # ejemplo si tenemos `lista = [1,2,3]`
        # esto se llama `unpacking`.
        # lo necesitamos porque nuestra funcion recibe N argumentos
        # no una lista de tamaño N.
        if self.value != None:
            return self.value 
        self.value = self.operation(*[node.eval(dict) for node in self.arguments])
        return self.value

    # hace una lista con todos los hijos
    def serialize(self):
        l = [self]
        for node in self.arguments:
            l.extend(node.serialize())
        return l

    # copia al nodo
    def copy(self):
        return deepcopy(self)

    # reemplaza el nodo por otro
    def replace(self, otherNode):
        # aqui estamos haciendo algo medio hacky.
        # la forma correcta seria tener una referencia al nodo padre y
        # reemplazarse a si mismo por otro.
        # por temas de mantener el codigo corto lo hacemos asi
        # pero no lo hagan en casa!
        assert isinstance(otherNode, Node)
        self.__class__ = otherNode.__class__
        self.__dict__ = otherNode.__dict__

    # cantidad de nodos en el arbol
    def size(self):
        if self.n > 0:
            return self.n
        self.n = 1 + sum([node.size() for node in self.arguments])
        return self.n

    # selecciona un nodo al azar y lo retorna
    def select(self, r=-1):
        p = r
        if r < 0:
            p = random.randint(0, self.size() - 1)
        if p == 0:
            return self
        else:
            count = 0
            for arg in self.arguments:
                size = arg.size()
                if p <= count + size:
                    return arg.select(p - count - 1)
                else:
                    count += size

    # selecciona un nodo al azar y lo reemplaza
    def select_replace(self, node, r=-1):
        p = r
        if r < 0:
            p = random.randint(0, self.size() - 1)

        self.n = 0 # resetea el tamaño para ser recalculado
        self.value = None # resetea el valor para ser recalculado

        if p == 0:
            self.replace(node)
        else:
            count = 0
            for arg in self.arguments:
                size = arg.size()
                if p <= count + size:
                    arg.select_replace(node, p - count - 1)
                    break
                else:
                    count += size


# esta clase representa todos los nodos quetienen 2 argumentos
class BinaryNode(Node):
    num_args = 2

    def __init__(self, function, left, right):
        # revisamos que todo sea un nodo y agregamos a las lista de
        # argumentos
        assert isinstance(left, Node)
        assert isinstance(right, Node)
        super(BinaryNode, self).__init__(function)
        self.arguments.append(left)
        self.arguments.append(right)


class AddNode(BinaryNode):
    def __init__(self, left, right):
        def _add(x, y):
            return x + y
        super(AddNode, self).__init__(_add, left, right)

    # esta es la funcion que define como se mostrara el nodo
    # como es un nodo que REPResenta la suma, lo mostramos como suma
    def __repr__(self):
        return "({} + {})".format(*self.arguments)


class SubNode(BinaryNode):
    def __init__(self, left, right):
        def _sub(x, y):
            return x - y
        super(SubNode, self).__init__(_sub, left, right)

    def __repr__(self):
        return "({} - {})".format(*self.arguments)


class MaxNode(BinaryNode):
    def __init__(self, left, right):
        def _max(x, y):
            return max(x, y)
        super(MaxNode, self).__init__(_max, left, right)

    def __repr__(self):
        return "max({}, {})".format(*self.arguments)


class MultNode(BinaryNode):
    def __init__(self, left, right):
        def _mult(x, y):
            return x * y
        super(MultNode, self).__init__(_mult, left, right)

    def __repr__(self):
        return "({} * {})".format(*self.arguments)


class DivNode(BinaryNode):
    def __init__(self, left, right):
        def _div(x, y):
            if y == 0:
                return "ERROR"
            return (x * 1.0) / y
        super(DivNode, self).__init__(_div, left, right)

    def __repr__(self):
        return "({} / {})".format(*self.arguments)


class TerminalNode(Node):
    # Este nodo representa una hoja de arbol. Es el nodo terminal
    # por lo que no tiene argumentos
    num_args = 0

    def __init__(self, value):
        # igual tenemos que representarlo como una funcion, por como
        # diseñamos el programa. Pero aqui va a ser una funcion vacia
        def _nothind(): pass
        super(TerminalNode, self).__init__(_nothind)
        self._value = value

    def __repr__(self):
        return str(self._value)

    def eval(self, dict={}):
        # la evaluacion de un nodo terminal es el valor que contiene
        if self._value in dict.keys():
            self.value = dict[self._value]
        else:
            self.value = self._value
        return self.value
