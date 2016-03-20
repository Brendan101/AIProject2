#File:        proj2.py
#Author:      Brendan Waters
#Email:       b101@umbc.edu
#Description:
#  This program takes command line arguments to search through a function
#  to optimize it for the minimum using one of the three algorithms:
#  Hillclimbing, Hillclimbing with Random Restarts, or Simulated
#  Annealing as specified by the user with parameters via command line
#  arguments.
#References:
#  Simulated Annealing info and pseudocode:
#    http://katrinaeg.com/simulated-annealing.html
#  Pyplot help
#    http://matplotlib.org/examples/mplot3d/surface3d_demo.html

import sys
import math
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

#This function calculates z = f(x, y) defined as
#r = sqrt(x**2+y**2)
#z = sin(x**2+3*y**2)/(0.1+r**2)+(x**2+5*y**2)*(e**(1-r**2)/2)
def test_function(x, y):
    x_square = math.pow(x, 2)
    y_square = math.pow(y, 2)
    r_square = x_square + y_square
    expr1 = math.sin(x_square + 3*y_square)
    expr2 = 0.1+r_square
    expr3 = x_square + 5*y_square
    expr4 = math.exp(1-r_square) / 2
    addend1 = expr1/expr2
    addend2 = expr3*expr4
    z = addend1 + addend2
    return z
    

#this function calculates the probability that a move will be taken in simulated annealing
#and then assigns the value of true or false to a boolean based on the probability calculated
#and returns whether or not the move should be taken
def take_move(temperature, z_current, z_next):
    
    #negative, because we are optimizing for the minimum
    probability = math.exp(-(z_next - z_current)/temperature)

    #get random value to see if it falls under the probability
    value = random.random()

    if value <= probability:
        return True
    else:
        return False

#This function searches a space by simple hillclimbing
def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):
    
    #keep track of path taken
    path = []

    x = xmax
    y = ymax
    climbing = True
    z = function_to_optimize(x, y)

    path.append((x, y, z))

    while(climbing):
        
        #calc current and next values
        if (x - step_size) >= xmin:
            next_x = x - step_size
        else:
            next_x = x
        if (y - step_size) >= ymin:
            next_y = y - step_size
        else:
            next_y = y
        z_next_x = function_to_optimize(next_x, y)
        z_next_y = function_to_optimize(x, next_y)
        
        #check which next is least, then compare that to the current value
        #if next move is lesser, move to it. If not then a local min is found and loop ends
        if z_next_x <= z_next_y:
            if z_next_x < z:
                x = next_x
                z = z_next_x
                path.append((x, y, z))
            else:
                climbing = False
        else:
            if z_next_y < z:
                y = next_y
                z = z_next_y
                path.append((x, y, z))
            else:
                climbing = False
    
    return path

#This function searches a space using hillclimbing with random restarts
def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
    
    #keep track of all hillclimb paths
    paths = []

    #list of tuples (x, y, z)
    extrema = []

    #do the hillclimbing starting from random positions
    for i in range (0, num_restarts):
        
        #get random starting coords
        x_start = random.uniform(xmin, xmax)
        y_start = random.uniform(ymin, ymax)
                
        #do search
        hillclimb_path = hill_climb(function_to_optimize, step_size, xmin, x_start, ymin, y_start)
        extremum = hillclimb_path[-1]
        x = extremum[0]
        y = extremum[1]
        z = extremum[2]
        extrema.append((x, y, z))

        #add this path into list
        for coordinate in hillclimb_path:
            paths.append(coordinate)

    #get minimum of all the searches
    minimum = extrema[0]
    for extremum in extrema:
        if extremum[2] < minimum[2]:
            minimum = extremum

    x = minimum[0]
    y = minimum[1]
    z = minimum[2]

    print("Minimum:\nx = ", x, "\ny = ", y, "\nz = ", z)
        
    return paths

#This function searches a space using simulated annealing
def simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):

    path = []
    
    #float
    temperature = float(max_temp)
    alpha = .99

    #starting point with value
    x = random.uniform(-2.5, 2.5)
    y = random.uniform(-2.5, 2.5)
    z = function_to_optimize(x, y)

    path.append((x, y, z))

    while temperature > .00001:
        
        #try 50 moves at each temperature
        for i in range(0, 50):
            x_next = random.uniform(-2.5, 2.5)
            y_next = random.uniform(-2.5, 2.5)
            z_next = function_to_optimize(x_next, y_next)

            if take_move(temperature, z, z_next):
                x = x_next
                y = y_next
                z = z_next
                path.append((x, y, z))

        temperature *= alpha

    print("Minimum:\nx = ", x, "\ny = ", y, "\nz = ", z)

    return path

def main():

    #check args
    if len(sys.argv) != 9:
        print("Usage: python proj2.py <step_size> <xmin> <xmax> <ymin> <ymax> <searchType> <num_restarts> <max_temp>\nValid Search Types: HC, RR, SA\nFor data that is not required for the chosen search type please enter 0 as a placeholder.")
        return 1

    #get args
    step_size = float(sys.argv[1])
    xmin = float(sys.argv[2])
    xmax = float(sys.argv[3])
    ymin = float(sys.argv[4])
    ymax = float(sys.argv[5])
    searchType = sys.argv[6]
    num_restarts = int(sys.argv[7])
    max_temp = int(sys.argv[8])
    
    #may be needed later
    random.seed()

    #call search
    if searchType == "HC":
        path = hill_climb(test_function, step_size, xmin, xmax, ymin, ymax)
    elif searchType == "RR":
        path = hill_climb_random_restart(test_function, step_size, num_restarts, xmin, xmax, ymin, ymax)
    elif searchType == "SA":
        path = simulated_annealing(test_function, step_size, max_temp, xmin, xmax, ymin, ymax)

    #make parallel x, y, z lists
    path_x = []
    path_y = []
    path_z = []
    for coordinate in path:
        path_x.append(coordinate[0])
        path_y.append(coordinate[1])
        path_z.append(coordinate[2])

    #done search, plot it
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    x = np.arange(xmin, xmax, 0.1)
    y = np.arange(ymin, ymax, 0.1)
    x, y = np.meshgrid(x, y)
    r = np.sqrt(x**2 + y**2)
    z = np.sin(x**2+3*y**2)/(0.1+r**2) + (x**2+5*y**2)*(np.exp(1-r**2)/2)
    surf = ax.plot_surface(x, y, z, rstride = 1, cstride = 1, cmap = cm.coolwarm, linewidth = 0, antialiased = False)
    ax.set_zlim(-1, 4)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink = 0.5, aspect = 5)

    #plot the path
    ax.plot(path_x, path_y, path_z, 'bo', markersize = 1)

    plt.show()

    return 0

if __name__ == "__main__": main()
