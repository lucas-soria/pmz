def open_file():
    with open('/home/lucas/Downloads/maze1.txt', 'r') as file:
        maze = file.read().strip('\n').split('\n')
        for i in range(len(maze)):
            maze[i] = list(maze[i])
            print(maze[i])
        solve(maze)


def posible_moves(maze, current, previous):
    up = (current[0] - 1, current[1])
    down = (current[0] + 1, current[1])
    right = (current[0], current[1] + 1)
    left = (current[0], current[1] - 1)
    moves = [up, down, left, right]
    posibles = []
    for move in moves:
        if move != previous and maze[move[0]][move[1]] != '#':
            if maze[move[0]][move[1]] == '+':
                pass
            posibles.append(move)
    for move in posibles:
        posible_moves(maze, move, current)
    print(posibles)


def solve(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '*':
                start = (i, j)
    moves = posible_moves(maze, start, start)
    print(moves)


if __name__ == "__main__":
    open_file()
