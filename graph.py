import copy
from enum import Enum


def adjacency_list_to_wrapper_str(adjacency_list):
    data = [[f'v_{i + 1}'] for i in range(len(adjacency_list))]
    columns_sizes = [0] * (len(data) + 1)
    for i in range(len(data)):
        columns_sizes[0] = max(columns_sizes[0], len(data[0]))
        for j in adjacency_list[i]:
            columns_sizes[1 + j] = max(columns_sizes[1 + j], len(data[i][j]))
            data[i].append(f'v_{j + 1}')
    result = ''
    for i, row in enumerate(data):
        result += ' '.join([element.ljust(columns_sizes[j]) for j, element in enumerate(row)])
        if i != len(data) - 1:
            result += '\r\n'
    return result


def matrix_to_wrapper_str(matrix, rows_infix, columns_infix):
    data = [[' '] * (len(matrix[0]) + 1) for _ in range(len(matrix) + 1)]
    for j in range(1, len(matrix[0]) + 1):
        data[0][j] = f'{columns_infix}_{j}'
    for i in range(1, len(matrix) + 1):
        data[i][0] = f'{rows_infix}_{i}'
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            data[i + 1][j + 1] = str(matrix[i][j])
    columns_sizes = [max([len(data[i][j]) for i in range(len(data))]) for j in range(len(data[0]))]
    result = ''
    for i, row in enumerate(data):
        result += data[i][0].ljust(columns_sizes[0])
        result += ' '.join([element.rjust(columns_sizes[j]) for j, element in enumerate(row[1:], start=1)])
        if i != len(data) - 1:
            result += '\r\n'
    return result


def adjacency_matrix_to_wrapper_str(adjacency_matrix):
    return matrix_to_wrapper_str(adjacency_matrix, 'v', 'v')


def incidence_matrix_to_wrapper_str(incidence_matrix):
    return matrix_to_wrapper_str(incidence_matrix, 'v', 'a')


def adjacency_list_to_adjacency_matrix(adjacency_list):
    result = [[0] * len(adjacency_list) for _ in range(len(adjacency_list))]
    for u, adjacency in enumerate(adjacency_list, start=0):
        for v in adjacency:
            result[u][v] += 1
    return result


def adjacency_list_to_incidence_matrix(adjacency_list):
    return adjacency_matrix_to_incidence_matrix(adjacency_list_to_adjacency_matrix(adjacency_list))


def adjacency_matrix_to_adjacency_list(adjacency_matrix):
    result = [[] for _ in range(len(adjacency_matrix))]
    for u in range(len(adjacency_matrix)):
        for v in range(len(adjacency_matrix)):
            for i in range(adjacency_matrix[u][v]):
                result[u].append(v)
    return result


def adjacency_matrix_to_incidence_matrix(adjacency_matrix):
    result = [[] for _ in range(len(adjacency_matrix))]
    for u in range(len(adjacency_matrix)):
        for v in range(len(adjacency_matrix)):
            if adjacency_matrix[u][v] != 0:
                if not (u > v and adjacency_matrix[v][u] == 1):
                    for i in range(len(result)):
                        result[i].append(0)
                    if u == v:
                        result[u][-1] = adjacency_matrix[u][v]
                    elif adjacency_matrix[v][u] == 0:
                        result[u][-1] = 1
                        result[v][-1] = -1
                    else:
                        result[u][-1] = result[v][-1] = 1
    return result


def incidence_matrix_to_adjacency_list(incidence_matrix):
    return adjacency_matrix_to_adjacency_list(incidence_matrix_to_adjacency_matrix(incidence_matrix))


def incidence_matrix_to_adjacency_matrix(incidence_matrix):
    result = [[0] * len(incidence_matrix) for _ in range(len(incidence_matrix))]
    for k_edge in range(len(incidence_matrix[0])):
        non_zeros = [(i, degree) for i in range(len(incidence_matrix)) if (degree := incidence_matrix[i][k_edge]) != 0]
        if len(non_zeros) == 1:
            i, degree = non_zeros[0]
            result[i][i] = degree
        else:
            (i, i_degree), (j, j_degree) = non_zeros[0], non_zeros[1]
            if i_degree == 1:
                result[i][j] = 1
            if j_degree == 1:
                result[j][i] = 1
    return result


class Graph:
    class State(Enum):
        ADJACENCY_LIST = 1
        ADJACENCY_MATRIX = 2
        INCIDENCE_MATRIX = 3

        @staticmethod
        def get_names():
            return ['adjacent list', 'adjacent matrix', 'incidence matrix']

        @staticmethod
        def get_by_name(name: str):
            name_to_state = {
                'adjacent list': Graph.State.ADJACENCY_LIST,
                'adjacent matrix': Graph.State.ADJACENCY_MATRIX,
                'incidence matrix': Graph.State.INCIDENCE_MATRIX
            }
            return name_to_state[name]

        @staticmethod
        def to_name(state):
            state_to_name = {
                Graph.State.ADJACENCY_LIST: 'adjacent list',
                Graph.State.ADJACENCY_MATRIX: 'adjacent matrix',
                Graph.State.INCIDENCE_MATRIX: 'incidence matrix'
            }
            return state_to_name[state]

    def __init__(self, list2: list, state: State, name: str = ''):
        self.list2 = list2
        self.state = state
        self.name = 'unnamed' if str == '' else name

    def __str__(self):
        title = f"Graph: '{self.name}'\r\n"
        state_to_wrapper_str = {
            Graph.State.ADJACENCY_LIST: adjacency_list_to_wrapper_str,
            Graph.State.ADJACENCY_MATRIX: adjacency_matrix_to_wrapper_str,
            Graph.State.INCIDENCE_MATRIX: incidence_matrix_to_wrapper_str
        }
        return title + state_to_wrapper_str[self.state](self.list2)

    @staticmethod
    def addition(graph):
        new_graph = copy.deepcopy(graph)
        state = new_graph.state
        new_graph.set_state(Graph.State.ADJACENCY_MATRIX)
        n = len(new_graph.vertices())
        for i in range(n):
            for j in range(n):
                new_graph.list2[i][j] = 1 if i != j and new_graph.list2[i][j] == 0 else 0
        new_graph.set_state(state)
        new_graph.set_name(f'{new_graph.name}_addition')
        return new_graph

    def union(self, other):
        new_graph = copy.deepcopy(self)
        new_graph_state, other_state = new_graph.state, other.state
        new_graph.set_state(Graph.State.INCIDENCE_MATRIX)
        other.set_state(Graph.State.INCIDENCE_MATRIX)
        n1, n2 = len(self.vertices()), len(other.vertices())
        n_e1, n_e2 = len(self.edges()), len(other.edges())
        for i in range(n1):
            new_graph.list2[i].append([0] * n_e2)
        for i in range(n2):
            new_graph.list2.append([0] * (n_e1 + n_e2))
        for i in range(n2):
            for j in range(n_e2):
                new_graph.list2[i + n1][j + n_e1] = other.list2[i][j]
        new_graph.set_state(new_graph_state)
        other.set_state(other_state)
        new_graph.set_name(f'{self.name}_union_{other.name}')
        return new_graph

    def connection(self, other):
        new_graph = self.union(other)
        n1, n2 = len(self.vertices()), len(other.vertices())
        n_e1, n_e2 = len(self.edges()), len(other.edges())
        for i in range(n1):
            for j in range(n_e2):
                new_graph.list2[i][j + n_e1] = 1
        for i in range(n2):
            for j in range(n_e1):
                new_graph.list2[i + n1][j] = 1
        new_graph.set_name(f'{self.name}_connection_{other.name}')
        return new_graph

    def set_state(self, state: State):
        if self.state == state:
            return
        list2_changers = {
            Graph.State.ADJACENCY_LIST: {
                Graph.State.ADJACENCY_MATRIX: adjacency_list_to_adjacency_matrix,
                Graph.State.INCIDENCE_MATRIX: adjacency_list_to_incidence_matrix
            },
            Graph.State.ADJACENCY_MATRIX: {
                Graph.State.ADJACENCY_LIST: adjacency_matrix_to_adjacency_list,
                Graph.State.INCIDENCE_MATRIX: adjacency_matrix_to_incidence_matrix
            },
            Graph.State.INCIDENCE_MATRIX: {
                Graph.State.ADJACENCY_LIST: incidence_matrix_to_adjacency_list,
                Graph.State.ADJACENCY_MATRIX: incidence_matrix_to_adjacency_matrix
            }
        }
        list2_changer = list2_changers[self.state][state]
        self.list2 = list2_changer(self.list2)
        self.state = state

    def set_name(self, name: str):
        self.name = 'unnamed' if str == '' else name

    def vertices(self):
        return list(range(len(self.list2)))

    def edges(self):
        state = self.state
        self.set_state(Graph.State.ADJACENCY_LIST)
        result = [(u, v) for u, adjacency in enumerate(self.list2) for v in adjacency]
        self.set_state(state)
        return result

    def identify_vertices(self, i, j):
        if i == j:
            return
        state = self.state
        self.set_state(Graph.State.ADJACENCY_MATRIX)
        list2 = self.list2
        for k in range(len(list2)):
            if k != i and k != j:
                if list2[j][k] == 1:
                    list2[i][k] = 1
                if list2[k][j] == 1:
                    list2[k][i] = 1
        if list2[i][j] == list2[j][i] == 1:
            list2[i][i] = 2
        elif list2[i][j] == 1 or list2[j][i] == 1:
            list2[i][i] = 1
        else:
            list2[i][i] = 0
        for k in range(len(list2)):
            list2[k][j] = 0
            list2[j][k] = 0
        self.set_state(Graph.State.INCIDENCE_MATRIX)
        del self.list2[j]
        self.set_state(state)

    def add_vertex(self, v):
        state = self.state
        self.set_state(Graph.State.INCIDENCE_MATRIX)
        self.list2.insert(v, [0] * len(self.list2[0]))
        self.set_state(state)

    def remove_vertex(self, v):
        state = self.state
        self.set_state(Graph.State.ADJACENCY_MATRIX)
        for i in range(len(self.list2)):
            self.list2[i][v] = 0
            self.list2[v][i] = 0
        self.set_state(Graph.State.INCIDENCE_MATRIX)
        del self.list2[v]
        self.set_state(state)

    def pull_of_edge(self, e_i):
        state = self.state
        self.set_state(Graph.State.INCIDENCE_MATRIX)
        for i in range(len(self.list2)):
            del self.list2[i][e_i]
        self.set_state(state)

    def add_edge(self, e):
        state = self.state
        self.set_state(Graph.State.ADJACENCY_MATRIX)
        i, j = e
        if i == j:
            self.list2[i][j] = min(2, self.list2[i][j] + 1)
        elif self.list2[i][j] == 0:
            self.list2[i][j] = 1
        self.set_state(state)

    def remove_edge(self, e_i):
        state = self.state
        self.set_state(Graph.State.INCIDENCE_MATRIX)
        for i in range(len(self.list2)):
            del self.list2[i][e_i]
        self.set_state(state)
