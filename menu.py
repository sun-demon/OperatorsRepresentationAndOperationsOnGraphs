from graph import Graph
import os
import pickle


def read_list2(filename):
    with open(filename, 'r') as file:
        return [[int(number) for number in line.split()] for line in file]


def write_list2(filename, matrix):
    with open(filename, 'w') as file:
        for i, row in enumerate(matrix):
            file.write(' '.join([str(number) for number in row]))
            if i != len(matrix) - 1:
                file.write('\n')


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def select(message):
    return int(input(f'Select {message} >'))


def select_item():
    return select('item')


def press_enter_for_continue():
    input('Press ENTER for continue...')


class Menu:
    __filename__ = 'graphs.bin'

    def __init__(self):
        if os.path.isfile(Menu.__filename__):
            with open(Menu.__filename__, 'rb') as file:
                self.graphs = pickle.load(file)
        else:
            self.graphs = []

    def __del__(self):
        with open(Menu.__filename__, 'wb') as file:
            pickle.dump(self.graphs, file)

    def run(self):
        while True:
            items_and_functions = [('new graph', Menu.new_graph)] if len(self.graphs) == 0 else [
                ('new graph', Menu.new_graph),
                ('existing graphs', Menu.existing_graphs),
                ('addition of graph', Menu.addition_graph),
                ('union of graphs', Menu.union_graphs),
                ('connection of graphs', Menu.connection_graphs)
            ]
            clear_screen()
            for i, item in enumerate(items_and_functions, start=1):
                print(f'{str(i).rjust(len(str(len(items_and_functions))))}) {item[0]}')
            print('0) exit')
            i = select_item()
            clear_screen()
            if i == 0:
                return
            items_and_functions[i - 1][1](self)

    def new_graph(self):
        clear_screen()
        filename = input('Enter filename with graph: ')
        states_names = Graph.State.get_names()
        print('Graph states:')
        for i, state_name in enumerate(states_names, start=1):
            print(f'{i}) {state_name}')
        i = int(input('Select graph input format: ')) - 1
        self.graphs.append(Graph(read_list2(filename), Graph.State.get_by_name(states_names[i])))

    def existing_graphs(self):
        while True:
            graphs_names = [graph.name for graph in self.graphs]
            clear_screen()
            for i, graph_name in enumerate(graphs_names, start=1):
                print(f"{i}) Graph: '{graph_name}'")
            print('0) back')
            i = select_item()
            if i == 0:
                return
            self.manage_graph(i - 1)

    def manage_graph(self, graph_i):
        while True:
            items = [
                ('print_info', Menu.print_graph_info),
                ('set_state', Menu.set_graph_state),
                ('rename', Menu.rename_graph),
                ('identify vertices', Menu.identify_vertices),
                ('add vertex', Menu.add_vertex),
                ('remove vertex', Menu.remove_vertex),
                ('pull off edge', Menu.pull_off_edge),
                ('add edge', Menu.add_edge),
                ('remove edge', Menu.remove_edge),
                ('save to file', Menu.save_to_file),
                ('remove graph', Menu.remove_graph_by_index)
            ]
            clear_screen()
            for i, item in enumerate(items, start=1):
                print(f'{str(i).rjust(len(str(len(items))))}) {item[0]}')
            print('0) back')
            i = select_item()
            clear_screen()
            if i == 0:
                return
            elif items[i - 1][1] == Menu.remove_graph_by_index:
                Menu.remove_graph_by_index(self, graph_i)
                return
            items[i - 1][1](self.graphs[graph_i])

    @staticmethod
    def print_graph_info(graph):
        print(graph)
        print()
        print(f'State: {Graph.State.to_name(graph.state)}')
        print(f'Vertices number: {len(graph.vertices())}')
        print(f'Edges number: {len(graph.edges())}')
        print()
        press_enter_for_continue()

    @staticmethod
    def set_graph_state(graph):
        print(f"Graph: '{graph.name}'")
        print(f'Old graph format: {Graph.State.to_name(graph.state)}')
        print('Graph formats:')
        states_names = Graph.State.get_names()
        for i, state_name in enumerate(states_names, start=1):
            print(f'{i}) {state_name}')
        i = select('new graph format')
        graph.set_state(Graph.State.get_by_name(states_names[i]))

    @staticmethod
    def rename_graph(graph):
        print(f"Old name: '{graph.name}'")
        name = input(f'Enter new graph name: ')
        graph.set_name(name)

    @staticmethod
    def identify_vertices(graph):
        vertices = graph.vertices()
        print(f'Vertices: {tuple(vertices)}')
        i = int(input(f'Enter first  vertex: '))
        j = int(input(f'Enter second vertex: '))
        if i == j:
            print('The same vertex')
            press_enter_for_continue()
            return
        graph.identify_vertices(i - 1, j - 1)
        print(f'The vertices v_{i} and v_{j} have been successfully identified to vertex v_{i}')
        press_enter_for_continue()

    @staticmethod
    def add_vertex(graph):
        vertices = graph.vertices()
        print(f'Possible positions: {tuple(vertices.append(len(vertices) + 1))}')
        i = select('position for new vertex')
        graph.add_vertex(i - 1)

    @staticmethod
    def remove_vertex(graph):
        print(f'Vertices: {tuple(graph.vertices())}')
        i = select('vertex for removing')
        graph.remove_vertex(i - 1)

    @staticmethod
    def pull_off_edge(graph):
        edges = graph.edges()
        print('Edges:')
        for i, e in enumerate(edges, start=1):
            print(f'{str(i).rjust(len(str(len(edges))))}) {e}')
        i = select('edge number for pull offing')
        graph.pull_of_edge(i - 1)

    @staticmethod
    def add_edge(graph):
        print(f'Vertices: {tuple(graph.vertices())}')
        i = select('first vertex')
        j = select('second vertex')
        graph.add_edge((i - 1, j - 1))

    @staticmethod
    def remove_edge(graph):
        edges = graph.edges()
        print('Edges:')
        for i, e in enumerate(edges, start=1):
            print(f'{str(i).rjust(len(str(len(edges))))}) {e}')
        i = select('edge number for removing')
        graph.remove_edge(i - 1)

    @staticmethod
    def save_to_file(graph):
        filename = input(f"Enter filename for saving graph '{graph.name}': ")
        write_list2(filename, graph.list2)

    def remove_graph_by_index(self, graph_i):
        del self.graphs[graph_i]

    def addition_graph(self):
        graphs = self.graphs
        print('Graphs:')
        for i, graph in enumerate(graphs, start=1):
            print(f"{str(i).rjust(len(str(len(graphs))))}) '{graph.name}'")
        i = select('graph for addition')
        graphs.append(Graph.addition(graphs[i - 1]))

    def union_graphs(self):
        graphs = self.graphs
        print('Graphs:')
        for i, graph in enumerate(graphs, start=1):
            print(f"{str(i).rjust(len(str(len(graphs))))}) '{graph.name}'")
        i = select('first graph for union')
        j = select('second graph for union')
        graphs.append(graphs[i - 1].union(graphs[j - 1]))

    # def intersection_graphs(self):
    #     pass
    #
    # def xor_graphs(self):
    #     pass

    def connection_graphs(self):
        graphs = self.graphs
        print('Graphs:')
        for i, graph in enumerate(graphs, start=1):
            print(f"{str(i).rjust(len(str(len(graphs))))}) '{graph.name}'")
        i = select('first graph for connection')
        j = select('second graph for connection')
        graphs.append(graphs[i - 1].union(graphs[j - 1]))
