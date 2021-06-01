from .Tree import Tree, Parent, Child


class Maze:

    def __init__(self, maze) -> None:
        self.maze = self.separator(maze)
        self.tree = None
        self.path = None

    def separator(self, maze) -> list:
        maze_as_table = []
        maze = maze.split('\n')
        for row in maze:
            maze_row = []
            for cell in row:
                maze_row.append(cell)
            if len(maze_row) != 0:
                maze_as_table.append(maze_row)
        return maze_as_table

    def posible_moves(self, current, previous, tree) -> Tree:
        up = (current[0] - 1, current[1])
        down = (current[0] + 1, current[1])
        right = (current[0], current[1] + 1)
        left = (current[0], current[1] - 1)
        moves = [up, down, left, right]
        posible = []
        for move in moves:
            if move != previous and self.maze[move[0]][move[1]] != '#':
                posible.append(move)
                if self.maze[move[0]][move[1]] == '+':
                    break
        if self.maze[current[0]][current[1]] == '+':
            tree = Parent(current)
            tree.add_node(Child('+'))
        else:
            if len(posible) == 0:
                tree = Child(current)
        for move in posible:
            parent = Parent(move)
            child = self.posible_moves(move, current, parent)
            tree.add_node(child)
        return tree

    def reverse_order(self, tree, path) -> list:
        path.append(tree.position)
        if tree.get_parent().position == '*':
            return path[::-1]
        return self.reverse_order(tree.get_parent(), path)

    def find_path(self, tree) -> None:
        if tree.is_parent():
            for child in tree.children:
                self.find_path(child)
        else:
            if tree.position == '+':
                self.path = self.reverse_order(tree.get_parent(), [])

    def solve(self) -> list:
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == '*':
                    start = (i, j)
        self.tree = Parent('*')
        start_tree = Parent(start)
        start_tree = self.posible_moves(start, start, start_tree)
        self.tree.add_node(start_tree)
        self.find_path(self.tree)
        return self.path
