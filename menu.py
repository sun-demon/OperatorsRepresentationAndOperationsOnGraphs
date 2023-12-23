from graph import (Graph, str_data_matrix_to_str)
import os
import pickle


def read_list2(filename: str) -> list:
    with open(filename, 'r') as file:
        return [[int(number) for number in line.split()] for line in file]


def write_list2(filename: str, matrix: list) -> None:
    with open(filename, 'w') as file:
        for i, row in enumerate(matrix):
            file.write(' '.join([str(number) for number in row]))
            if i != len(matrix) - 1:
                file.write('\n')


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def select(message: str) -> int:
    return int(input(f'Select {message} >'))


def select_item() -> int:
    return select('item')


def press_enter_for_continue() -> None:
    input('Press ENTER for continue...')


class Menu:
    __filename__ = 'graphs.bin'

    def __init__(self):
        if os.path.isfile(Menu.__filename__):
            with open(Menu.__filename__, 'rb') as file:
                self.graphs: list = pickle.load(file)
        else:
            self.graphs = []

    def __del__(self):
        with open(Menu.__filename__, 'wb') as file:
            pickle.dump(self.graphs, file)

    @staticmethod
    def select_item_with_backing_and_double_clearing(items_and_functions: list) -> int:
        clear_screen()
        just = len(str(len(items_and_functions)))
        for i, item in enumerate(items_and_functions, start=1):
            print(f'{str(i).rjust(just)}) {item[0]}')
        print(f"{'0'.rjust(just)}) exit")
        i = select_item()
        clear_screen()
        return i

    def run(self):
        while True:
            items_and_functions = [('new graph', self.new_graph)] if len(self.graphs) == 0 else [
                ('new graph', self.new_graph),
                ('existing graphs', self.existing_graphs),
                ('addition of graph', self.addition_graph),
                ('union of graphs', self.union_graphs),
                ('connection of graphs', self.connection_graphs)
            ]
            i = Menu.select_item_with_backing_and_double_clearing(items_and_functions)
            if i == 0:
                return
            if i not in range(1, len(items_and_functions) + 1):
                print('Incorrect item number')
                press_enter_for_continue()
            else:
                items_and_functions[i - 1][1]()

    def new_graph(self) -> None:
        filename = input('Enter filename with graph: ')
        states_names = Graph.State.get_names()
        print('Graph states:')
        for i, state_name in enumerate(states_names, start=1):
            print(f'{i}) {state_name}')
        i = int(input('Select graph input format: ')) - 1
        self.graphs.append(Graph(read_list2(filename), Graph.State.get_by_name(states_names[i]), filename))

    def existing_graphs(self) -> None:
        while True:
            if len(self.graphs) == 0:
                return
            graphs_names = [graph.name for graph in self.graphs]
            clear_screen()
            for i, graph_name in enumerate(graphs_names, start=1):
                print(f"{i}) Graph: '{graph_name}'")
            print('0) back')
            i = select_item()
            if i == 0:
                return
            self.manage_graph(i - 1)

    def manage_graph(self, graph_i: int) -> None:
        while True:
            items_and_functions = [
                ('print_info', Menu.print_graph_info),
                ('set_state', Menu.set_graph_state),
                ('rename', Menu.rename_graph),
                ('identify vertices', Menu.identify_vertices),
                ('add vertex', Menu.add_vertex),
                ('print vertices degrees', Menu.print_vertices_degrees),
                ('remove vertex', Menu.remove_vertex),
                ('pull off edge', Menu.pull_off_edge),
                ('add directed edge', Menu.add_directed_edge),
                ('remove directed edge', Menu.remove_directed_edge),
                ('save to file', Menu.save_to_file),
                ('remove graph', Menu.remove_graph_by_index)
            ]
            i = Menu.select_item_with_backing_and_double_clearing(items_and_functions)
            if i == 0:
                return
            elif items_and_functions[i - 1][1] == Menu.remove_graph_by_index:
                Menu.remove_graph_by_index(self, graph_i)
                return
            items_and_functions[i - 1][1](self.graphs[graph_i])

    @staticmethod
    def print_graph_info(graph: Graph) -> None:
        print(graph)
        print()
        print(f'State: {Graph.State.to_name(graph.state)}')
        print(f'Vertices number: {len(graph.vertices())}')
        print(f'Edges number: {graph.edges_number()}')
        print(f'Directed edges number: {len(graph.directed_edges())}')
        print()
        press_enter_for_continue()

    @staticmethod
    def set_graph_state(graph: Graph) -> None:
        print(f"Graph: '{graph.name}'")
        print(f'Old graph format: {Graph.State.to_name(graph.state)}')
        print('Graph formats:')
        states_names = Graph.State.get_names()
        for i, state_name in enumerate(states_names, start=1):
            print(f'{i}) {state_name}')
        i = select('new graph format')
        if i != 0:
            graph.set_state(Graph.State.get_by_name(states_names[i - 1]))

    @staticmethod
    def rename_graph(graph: Graph) -> None:
        print(f"Old name: '{graph.name}'")
        name = input(f'Enter new graph name: ')
        graph.set_name(name)

    @staticmethod
    def identify_vertices(graph: Graph) -> None:
        print(f'Vertices: {(vertex + 1 for vertex in graph.vertices())}')
        i = select('first  vertex')
        if i not in range(1, len(graph.vertices()) + 1):
            print(f'Incorrect first vertex number')
            press_enter_for_continue()
            return
        j = select('second vertex')
        if j not in range(1, len(graph.vertices()) + 2):
            print(f'Incorrect second vertex number')
            press_enter_for_continue()
            return
        if i == j:
            print('The same vertex')
            press_enter_for_continue()
            return
        graph.identify_vertices(i - 1, j - 1)
        print(f'The vertices v_{i} and v_{j} have been successfully identified to vertex v_{i}')
        press_enter_for_continue()

    @staticmethod
    def add_vertex(graph: Graph) -> None:
        positions = [vertex + 1 for vertex in graph.vertices()]
        positions.append(len(positions) + 1)
        print(f'Possible positions: {tuple(positions)}')
        i = select('position for new vertex')
        if i not in range(1, len(graph.vertices()) + 2):
            print(f'Incorrect position')
            press_enter_for_continue()
            return
        graph.add_vertex(i - 1)

    @staticmethod
    def print_vertices_degrees(graph: Graph) -> None:
        n = len(graph.vertices())
        directed_edges = graph.directed_edges()
        data = [[' '] * (n + 1) for _ in range(3)]
        for j in range(1, n + 1):
            data[0][j] = f'v_{j}'
        data[1][0] = 'in  degree'
        data[2][0] = 'out degree'
        for v in range(n):
            data[1][v + 1] = str(sum([1 for i, j in directed_edges if j == v]))
            data[2][v + 1] = str(sum([1 for i, j in directed_edges if i == v]))
        print(str_data_matrix_to_str(data))
        press_enter_for_continue()

    @staticmethod
    def remove_vertex(graph: Graph) -> None:
        print(f'Vertices: {tuple([vertex + 1 for vertex in graph.vertices()])}')
        i = select('vertex for removing')
        if i not in range(1, len(graph.vertices()) + 1):
            print(f'Incorrect vertex number')
            press_enter_for_continue()
            return
        graph.remove_vertex(i - 1)

    @staticmethod
    def __print_directed_edges_items__(graph: Graph) -> None:
        directed_edges = graph.directed_edges()
        print('Directed edges:')
        for i, e in enumerate(directed_edges, start=1):
            print(f'{str(i).rjust(len(str(len(directed_edges))))}) ({e[0] + 1}, {e[1] + 1})')

    @staticmethod
    def pull_off_edge(graph: Graph) -> None:
        Menu.__print_directed_edges_items__(graph)
        i = select('directed edge number for pull offing')
        if i not in range(1, len(graph.directed_edges()) + 1):
            print('Incorrect directed edge number')
            press_enter_for_continue()
            return
        graph.pull_of_edge(graph.directed_edges()[i - 1])

    @staticmethod
    def add_directed_edge(graph: Graph) -> None:
        print(f'Vertices: {tuple([vertex + 1 for vertex in graph.vertices()])}')
        i = select('first vertex')
        if i not in range(1, len(graph.vertices()) + 1):
            print(f'Incorrect first vertex number')
            press_enter_for_continue()
            return
        j = select('second vertex')
        if j not in range(1, len(graph.vertices()) + 1):
            print(f'Incorrect second vertex number')
            press_enter_for_continue()
            return
        graph.add_directed_edge((i - 1, j - 1))

    @staticmethod
    def remove_directed_edge(graph: Graph) -> None:
        Menu.__print_directed_edges_items__(graph)
        i = select('edge number for removing')
        if i not in range(1, len(graph.directed_edges()) + 1):
            print(f'Incorrect edge number')
            press_enter_for_continue()
            return
        graph.remove_directed_edge(graph.directed_edges()[i - 1])

    @staticmethod
    def save_to_file(graph: Graph) -> None:
        filename = input(f"Enter filename for saving graph '{graph.name}': ")
        write_list2(filename, graph.list2)

    def remove_graph_by_index(self, graph_i: int) -> None:
        if graph_i not in range(len(self.graphs)):
            print('Incorrect graph number')
            press_enter_for_continue()
            return
        del self.graphs[graph_i]

    def addition_graph(self) -> None:
        graphs = self.graphs
        print('Graphs:')
        for i, graph in enumerate(graphs, start=1):
            print(f"{str(i).rjust(len(str(len(graphs))))}) '{graph.name}'")
        i = select('graph for addition')
        if i not in range(1, len(self.graphs) + 1):
            print('Incorrect graph number')
            press_enter_for_continue()
            return
        graphs.append(Graph.addition(graphs[i - 1]))

    def union_graphs(self) -> None:
        graphs = self.graphs
        print('Graphs:')
        for i, graph in enumerate(graphs, start=1):
            print(f"{str(i).rjust(len(str(len(graphs))))}) '{graph.name}'")
        i = select('first graph for union')
        if i not in range(1, len(self.graphs) + 1):
            print('Incorrect first graph number')
            press_enter_for_continue()
            return
        j = select('second graph for union')
        if j not in range(1, len(self.graphs) + 1):
            print('Incorrect second graph number')
            press_enter_for_continue()
            return
        graphs.append(graphs[i - 1].union(graphs[j - 1]))

    # def intersection_graphs(self):
    #     pass
    #
    # def xor_graphs(self):
    #     pass

    def connection_graphs(self) -> None:
        graphs = self.graphs
        print('Graphs:')
        for i, graph in enumerate(graphs, start=1):
            print(f"{str(i).rjust(len(str(len(graphs))))}) '{graph.name}'")
        i = select('first graph for connection')
        if i not in range(1, len(self.graphs) + 1):
            print('Incorrect first graph number')
            press_enter_for_continue()
            return
        j = select('second graph for connection')
        if j not in range(1, len(self.graphs) + 1):
            print('Incorrect second graph number')
            press_enter_for_continue()
            return
        graphs.append(graphs[i - 1].connection(graphs[j - 1]))
