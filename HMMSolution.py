#Himadri Narasimhamurthy
#Function to Print out the solution from HMM

from Maze import Maze
from HMM import HMM

def print_sol(hmm):

    #gets the hmm sequence
    seq = hmm.get_sequence()
    print(seq)
    string = "The robot is at the bolded location. HMM estimates the robot's location at the location in *s.\n" + "If there is no *'d location, HMM estimates the loc with highest probability"
    string2 = ""

    #write per state
    for i in range(len(hmm.forwardstates)):
        ind = i-1

        #add header to each state
        string += "\nStep " + str(i)

        #outputs move, location, and sensor value
        string += " : move: " + str(hmm.move_seq[ind-1]) + "\n"
        string += " Robot is at " + "(" + str(hmm.robotlocs[ind][0]) + ", " + \
             str(hmm.robotlocs[ind][1]) + ")" + " and the color sensor says " \
             + hmm.color_sequence[ind]


        string += "\n" + " " + "\n"
        #loop through the tiles and add them to string
        for y in range(hmm.maze.height, 0, -1):
            string += " "
            for x in range(hmm.maze.width):
                coords = hmm.maze.index(x,y)

                #to debug the problem of getting negative coords first
                if coords>=0:

                    if len(hmm.robotlocs) >= i > 0 and hmm.robotlocs[ind] == (x, y):
                        string += "\033[1m "
                    else:
                        string += " "
                    if i > 0 and seq[ind] == coords:
                        string += str("*%.4f" % hmm.forwardstates[i][coords]) + "(" + hmm.maze.map[coords] + ")" + "* \033[0m"
                    else:
                        string += str("%.4f" % hmm.forwardstates[i][coords]) + "(" + hmm.maze.map[coords] + ")" + "  \033[0m"
                elif coords < 0:
                    if len(hmm.robotlocs) >= i > 0 and hmm.robotlocs[ind] == (x, y):
                        string2 += "\033[1m "
                    else:
                        string2 += " "
                    if i > 0 and seq[ind] == coords:
                        string2 += str("*%.4f" % hmm.forwardstates[i][coords]) + "(" + hmm.maze.map[coords] + ")" + "* \033[0m"
                    else:
                        string2 += str("%.4f" % hmm.forwardstates[i][coords]) + "(" + hmm.maze.map[coords] + ")" + "  \033[0m"

            string += "\n"
        string += " " + string2 + "\n"
        string2 = ""
    return string

#test code

maze1 = Maze("maze2.maz")
hmm1 = HMM(maze1)

hmm1.run()
print(print_sol(hmm1))