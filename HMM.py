from Maze import *
import numpy as np

#Himadri Narasimhamurthy
#HMM Class
#includes filtering, probability calc, and simulation

class HMM:
    def __init__(self, maze, initial = (0,0), move_seq = []):
        self.maze = maze

        self.moves = [(0,1),(0,-1),(1,0),(-1,0)]
        self.accuracy = .88
        self.initial_loc = initial
        self.move_seq = move_seq

        self.forwardstates = []
        
        #populate backwards messages
        self.bprobs = []
        self.bprobs.append([1 for i in range(len(self.maze.dist))])

        #we create the transition matrix
        self.trans = [[0 for i in range(len(self.maze.dist))] for j in range(len(self.maze.dist))]

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    for neighbor in self.moves:
                        if self.maze.is_floor(x + neighbor[0], y + neighbor[1]):
                            new_ind = self.maze.index(x + neighbor[0], y + neighbor[1])

                            #in the case that we can move, we set prob value to 1/4 with the indexes of new matrix
                            self.trans[new_ind][self.maze.index(x, y)] += 1/len(self.maze.colors)
                        else:
                            self.trans[self.maze.index(x, y)][self.maze.index(x, y)] += 1/len(self.maze.colors)

        #now we make a colors matrix - dictionary
        self.colormatrix = {}
        for color in self.maze.colors:

            color_matrix = [0 for i in range(len(self.maze.dist))]

            for x in range(self.maze.width):
                for y in range(self.maze.height):
                    if self.maze.is_floor(x, y):
                        coords = self.maze.index(x, y)

                        #if the color is same then set prob value as 0.88
                        if self.maze.map[coords] == color:
                            color_matrix[coords] = self.accuracy
                        else:
                            color_matrix[coords] = (1 - self.accuracy) / 3
            self.colormatrix[color] = color_matrix

        self.robotlocs = self.locate_bot()
        self.color_sequence = self.get_colors()

    #calculate the x and y lovations after the move sequence moves
    def locate_bot(self):
        locs = []

        cur_loc = (self.initial_loc[0], self.maze.height - self.initial_loc[1] - 1)
        locs.append(cur_loc)

        #move if not floor - update location
        for move in self.move_seq:
            if self.maze.is_floor(cur_loc[0] + move[0], cur_loc[1] + move[1]):
                cur_loc = (cur_loc[0] + move[0], cur_loc[1] + move[1])
            else:
                cur_loc = cur_loc

            locs.append(cur_loc)

        return locs

    #get color sensor input after each move sequence move
    def get_colors(self):
        color_seq = []
        for loc in self.robotlocs:
            color = ""

            #accuracy check
            if random.uniform(0, 1) < self.accuracy:
                if self.maze.is_floor(loc[0],loc[1]):
                    coords = self.maze.index(loc[0],loc[1])
                    color = self.maze.map[coords]
            else:
                color = random.choice(self.maze.colors)

            color_seq.append(color)
        return color_seq

    # the movement step - calculate forward row mat and backwards col mat
    def forward_backward(self):

        #first, original distribution
        self.forwardstates.append(self.maze.dist)

        #forward step
        for i in range(len(self.color_sequence)):

            #dot the trans model with each state and then filter
            state = np.dot(self.trans, self.forwardstates[i])
            self.forwardstates.append(state)

            #filtering using matrix multiplication
            m1 = self.colormatrix[self.color_sequence[i]]
            m2 = self.forwardstates[i+1]
            self.forwardstates[i+1] = np.multiply(m1, m2)

            # normalize the distribution
            den = sum(self.forwardstates[i+1])
            self.forwardstates[i+1] = self.forwardstates[i+1] / den
            
        #backwards step
        for i in range(len(self.color_sequence)):
            #get negative value as column index
            c = self.color_sequence[-i - 1]

            #calculate in the same way as forwards filtering but with back sequences
            b = np.multiply(self.colormatrix[c], self.bprobs[i])
            self.bprobs.append(b)

    #smooth the two row and col matrices
    def smoothing(self):
        self.forward_backward()

        #go through the len of the moves
        for i in range(len(self.color_sequence)):
            #save back and forward indeces
            rind = i+1
            cind = -i-1

            #dot the trans and back probabilities to get the proper back prob
            back = np.dot(self.trans, self.bprobs[cind])

            #save the states by multiplying back and forward
            self.forwardstates[rind] = np.multiply(back, self.forwardstates[rind])

            #normalize the distribution
            den = sum(self.forwardstates[rind])
            self.forwardstates[rind] = self.forwardstates[rind] / den

    # returns robot's estimated locations
    def get_sequence(self):
         # simple method of stepping through and getting highest probabilities at each step
        max_seq = []

        for i in self.forwardstates:
            hprob = 0
            ind = 0
            print(i)
            for j in range(len(i)):
                if i[j]>hprob:
                    hprob = i[j]
                    ind = j
            print(i[ind])
            max_seq.append(ind)

        return max_seq


    def get_possible_moves(self, index):
        poss = []

        #get x and y location and update possible moves
        y = index // self.maze.height
        x = index % self.maze.height * y
        for move in self.moves:
            if self.maze.is_floor(x + move[0], y + move[1]):
                m = self.maze.index(x + move[0], y + move[1])
            else:
                m = index
            poss.append(m)
        return poss

    #runs the robot's movement for 10 steps.
    def run(self):
        i = self.maze.create_rand_initial()
        m = self.maze.create_rand_moves(10)

        self.initial_loc = i
        self.move_seq = m

        self.robotlocs = self.locate_bot()
        self.color_sequence = self.get_colors()

        self.smoothing()


# Some test code

if __name__ == "__main__":
    test_maze1 = Maze("maze2.maz")
    hmm= HMM(test_maze1)
