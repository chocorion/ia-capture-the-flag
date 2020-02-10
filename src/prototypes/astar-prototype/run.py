import os
import sys
import timeit
from board import read_from_txt, create_neighbors, draw_board
from a_star import a_star

# Read board number from command line
if len(sys.argv) == 3:
    board = sys.argv[1]
    number = sys.argv[2]
else:
    print("Select a board. Example: 'python3 run.py 1 1'")
    sys.exit()

# Filename for reading board config
file_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(file_dir, 'boards/board-{0}-{1}.txt'.format(board, number))

# Create list with nodes
nodeGraph = read_from_txt(filename)

# Create neighbor list for all nodes (no need now)
#for node in nodeGraph:
#   create_neighbors(node, nodeGraph)

# Get start and goal node
start = list(filter(lambda n: n.cellContent == 'A', nodeGraph))[0]
goal  = list(filter(lambda n: n.cellContent == 'B', nodeGraph))[0]

# Get shortest path A star
starttime = timeit.default_timer()
print("The start time for A STAR is :",starttime)

res_a_star = a_star(start, goal, nodeGraph)

starttime = timeit.default_timer()
print("The time difference for A STAR is :", timeit.default_timer()-starttime)

# Get visualization of path
draw_board(res_a_star.path, res_a_star.border, res_a_star.closed, nodeGraph,'A-star-board-{0}-{1}'.format(board, number))

