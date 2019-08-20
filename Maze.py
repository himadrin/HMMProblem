from time import sleep
import random

# Maze.py
# modified from original mazeworld
#  original version by db, Fall 2017
#  Feel free to modify as desired.

# Maze objects are for loading and displaying mazes, and doing collision checks.
#  They are not a good object to use to represent the state of a robot mazeworld search
#  problem, since the locations of the walls are fixed and not part of the state;
#  you should do something else to represent the state. However, each Mazeworldproblem
#  might make use of a (single) maze object, modifying it as needed
#  in the process of checking for legal moves.

# Test code at the bottom of this file shows how to load in and display
#  a few maze data files (e.g., "maze1.maz", which you should find in
#  this directory.)

#  the order in a tuple is (x, y) starting with zero at the bottom left

# Maze file format:
#    # is a wall
#    r/g/b is a floor
# the command \robot x y adds a robot at a location. The first robot added
# has index 0, and so forth.

#moves are in [(0,1), (0,-1)] form
class Maze:

    # internal structure:
    #   self.walls: set of tuples with wall locations
    #   self.width: number of columns
    #   self.rows

    def __init__(self, mazefilename):

        f = open(mazefilename)
        lines = []
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            elif line[0] == "\\":

                parms = line.split()
                x = int(parms[1])
                y = int(parms[2])

            else:
                lines.append(line)
        f.close()

        self.width = len(lines[0])
        self.height = len(lines)

        self.map = list("".join(lines))


        self.colors = ["b", "r", "g", "y"]

        self.num_floors = 0
        self.num_floor()

        self.dist = []
        self.distribution()

    # gets the index at
    #def index(self, x, y):
     #   return (x * self.height) + y

    def index(self, x, y):
        return (self.height - y - 1) * self.width + x

    # creates random initial location
    def create_rand_initial(self):
        while True:
            if self.is_floor(random.randint(0,self.width-1), random.randint(0,self.height-1)):
                loc = (random.randint(0,self.width-1), random.randint(0,self.height-1))
                break

        return loc

    #it then appends a series of random moves to the moce list
    def create_rand_moves(self, num):
        moves = []
        for i in range(num):
            m = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            moves.append(m)

        return moves

    # returns True if the location is a floor
    def is_floor(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        if self.map[self.index(x, y)] == "#":
            return False

        return True

    #get total number of floors
    def num_floor(self):
        floors = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.is_floor(x,y):

                    floors = floors+1
        self.num_floors = floors

    #calculate the original distribution of the entire map
    def distribution(self):
        distribution = []

        for x in range(self.width):
            for y in range(self.height):
                if self.is_floor(x,y):
                    distribution.append(1/self.num_floors)
                else:
                    distribution.append(0)

        self.dist = distribution


if __name__ == '__main__':
    test = Maze("maze1.maz")
    print(test.index(0,0))
    print(test.index(2,5))
    print(test.is_floor(0,5))
    print(test.is_floor(1,5))
    print(test.map[2])

