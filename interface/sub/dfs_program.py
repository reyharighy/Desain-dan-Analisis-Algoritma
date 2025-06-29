"""Module to simulate user interaction with DFS algorithm"""

from interface.core.base_program import BaseProgram
from interface.contents import content_dictionary, subcontent_dictionary
from tools.algorithms.depth_first_search import DepthFirstSearch
from tools.api.object import Vertex

class DFSProgram(BaseProgram):
    """A class to provide a DFS-related operations to user."""

    def __init__(self) -> None:
        super().__init__()
        self.__dfs = DepthFirstSearch()
        self._append_success_message(f"Activate subprogram: {self.__repr__()}")

    def __repr__(self) -> str:
        return "Depth-First Search"

    def __execute_process(self):
        """Executes the subprocess depending on the user input."""
        option_input = self._option_entry_handler()

        match option_input:
            case 1:
                self.__create_vertex()
                self._reset_external_contexts()
                return
            case 2:
                self.__create_edge()
                self._reset_external_contexts()
                return
            case 3:
                self.__dfs.create_graph_from_problem_statement(1)
                self._append_success_message("Graph has successfully been created")
                return
            case 4:
                self.__dfs.visualize()
                return
            case 5:
                self.__run()
                self._reset_external_contexts()
                return
            case 6:
                self._extrn.resume = False
                return
            case None:
                self._base.message = "Invalid: Input must not be empty"
            case -1:
                self._base.message = "Invalid: Only accept numeric type"
            case _:
                self._base.message = f"Invalid: No option number {option_input}"

        self._append_error_message(self._base.message)

    def start(self):
        """A section to start the DFS program."""
        content = content_dictionary['dfs']
        title: str = content['title']
        body: str = content['body']

        while self._extrn.resume:
            self._refresh_display(title, self.__dfs.definition('dfs') + body)
            self.__execute_process()

    def save_exit(self):
        """Saves configuration made after exiting the program."""

    def __vertex_creation_session(self, label: str):
        """Provides a session when creating a vertex."""
        vertex = self.__dfs.add_vertex(label)

        if isinstance(vertex, str):
            self._append_error_message(vertex)
        else:
            if vertex:
                self._append_success_message(f"Vertex({label}) has been created")
            else:
                self._append_error_message(f"Invalid: Vertex({label}) already exists")

            self._extrn.resume = False

    def __vertex_creation_process(self):
        """Executes a process of creating a vertex."""
        label_input = input("Enter vertex label: ")
        self._loading()
        self.__vertex_creation_session(label_input)

    def __create_vertex(self):
        """Simulates a process of adding a new vertex."""
        title: str = " CREATE A NEW VERTEX "

        while self._extrn.resume:
            self._refresh_display(title, self.__dfs.definition('dfs'))
            self.__vertex_creation_process()

    def __edge_complement_exists(self, source: Vertex, destination: Vertex) -> bool:
        """Checkes if there's a complement of such edge."""
        for edge in destination.get_edges():
            if edge.get_destination() is source:
                return True

        return False

    def __edge_content(self, src: Vertex | None, dest: Vertex | None) -> str:
        """Provides contens when operation with an edge."""
        body: str = self.__dfs.definition('dfs')
        source_definition = None
        destination_definition = None

        if isinstance(src, Vertex):
            source_definition = src.definition('dfs')

        source_prompt: str = '\n' + f"\tSource:\n\t  - {source_definition}"
        body += source_prompt

        if isinstance(dest, Vertex):
            destination_definition = dest.definition('dfs')

        destination_prompt: str = '\n' + f"\tDestination:\n\t  - {destination_definition}"
        body += destination_prompt + '\n'

        return body

    def __edge_creation_content(self, src: Vertex | None, dest: Vertex | None, valid: bool) -> str:
        """Provides a customized content when adding a new edge."""
        body = self.__edge_content(src, dest)

        if isinstance(src, Vertex) and isinstance(dest, Vertex) and valid:
            if not self.__edge_complement_exists(src, dest):
                body += subcontent_dictionary['two_direction_edge']

        return body

    def __vertex_retrieval_session(self, search_for: str | None = None) -> Vertex | None:
        """Provides a session when retrieving a vertex."""
        if search_for:
            search_for = ' ' + search_for + ' '
        else:
            search_for = ' '

        label_input = input(f"Enter{search_for}vertex label: ")
        self._loading()

        vertex = self.__dfs.get_vertex(label_input)

        if isinstance(vertex, str):
            self._append_error_message(vertex)
        elif vertex is None:
            self._append_error_message(f"Invalid: Vertex({label_input}) is not found")
        else:
            self._append_success_message(f"Vertex({label_input}) is found")
            return vertex

        return None

    def __edge_exists(self, source: Vertex, destination: Vertex) -> bool:
        """Checks if such edge is valid"""
        for edge in source.get_edges():
            if edge.get_destination() is destination:
                src_label, dest_label = source.get_label(), destination.get_label()
                self._base.message = f"Invalid: Edge({src_label}, {dest_label}) already exists"
                self._append_error_message(self._base.message)
                self._extrn.resume = False
                return True

        return False

    def __edge_creation_session(self, source: Vertex, destination: Vertex, two_direction: bool):
        """Provides a session when creating an edge."""
        if two_direction:
            edge_label_1 = f"Edge({source.get_label()}, {destination.get_label()})"
            edge_label_2 = f"Edge({destination.get_label()}, {source.get_label()})"
            edge_label = f"{edge_label_1} and {edge_label_2}"
            self._append_success_message(f"{edge_label} have successfully been created")
            return

        edge_label = f"Edge({source.get_label()}, {destination.get_label()})"
        self._append_success_message(f"{edge_label} has successfully been created")

    def __edge_creation_process(self, source: Vertex, destination: Vertex):
        """Executes a process of creating an edge upon successful validation."""
        if self.__edge_complement_exists(source, destination):
            self.__dfs.add_edge(source, destination)
            self._extrn.resume = False
            self.__edge_creation_session(source, destination, self._edg.two_direction)
            return

        option_input = self._option_entry_handler()

        match option_input:
            case 1:
                self.__dfs.add_edge(source, destination)
                self._extrn.resume = False
                self.__edge_creation_session(source, destination, self._edg.two_direction)
                return
            case 2:
                self.__dfs.add_edge(source, destination, (1, 1))
                self._edg.two_direction = True
                self._extrn.resume = False
                self.__edge_creation_session(source, destination, self._edg.two_direction)
                return
            case None:
                self._base.message = "Invalid: Input must not be empty"
            case -1:
                self._base.message = "Invalid: Only accept numeric type"
            case _:
                self._base.message = f"Invalid: No option number {option_input}"

        self._append_error_message(self._base.message)

    def __create_edge(self):
        """Simulates a process of adding a new edge."""
        if len(self.__dfs.get_vertices()) < 2:
            self._append_error_message("Invalid: Graph must contain at least two vertices")
            return

        title: str = " CREATE A NEW EDGE "
        source: Vertex | None = None
        destination: Vertex | None = None

        while self._extrn.resume:
            body = self.__edge_creation_content(source, destination, self._extrn.valid)
            self._refresh_display(title, body)

            if source is None:
                source = self.__vertex_retrieval_session("source")

            elif destination is None:
                destination = self.__vertex_retrieval_session("destination")

            elif source and destination and not self._extrn.valid:
                self._extrn.valid = not self.__edge_exists(source, destination)

            elif self._extrn.valid:
                self.__edge_creation_process(source, destination)

    def __check_edges(self) -> bool:
        """Checks if graph has a vertex that has at least one edge."""
        for vertex in self.__dfs.get_vertices():
            if vertex.get_edges():
                return True

        return False

    def __run(self):
        """Simulate a process of running DFS on graph."""
        if not self.__check_edges():
            self._append_error_message("Invalid: Graph must contain at least one edge")
            return

        title: str = " RUN DEPTH-FIRST SEARCH "
        start: Vertex | None = None

        while self._extrn.resume:
            self._refresh_display(title, self.__dfs.definition("dfs"))

            if start is None:
                start = self.__vertex_retrieval_session("start")

            elif isinstance(start, Vertex):
                self.__dfs.run(start)
                self._extrn.resume = False
