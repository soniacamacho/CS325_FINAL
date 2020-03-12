# *****************************************************************************
# CS 325 FINAL PROJECT TRAVELING SALESMAN PROBLEM
# BY : SONIA CAMACHO OWEN MARKLEY ANJALI Vasisht
# *****************************************************************************
import math
import sys
import time
from timeit import default_timer


class City:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.visited = False

    def __str__(self):
        return f"City {self.id} {self.x} {self.y} {self.visited}"


# *****************************************************************************
# Function to get the distance between two points 
# ******************************************************************************
def calculateDistance(city1, city2):
    x_distance = abs(city1['x'] - city2['x'])
    y_distance = abs(city1['y'] - city2['y'])
    return int(round(math.sqrt(x_distance * x_distance + y_distance * y_distance)))


# *****************************************************************************
# Function to get the total distance, this was outlined in the program sepcification
# ******************************************************************************
def calculateTotalDistance(route):
    total = 0
    for idx in range(0, len(route) - 1):
        total += calculateDistance(route[idx], route[idx + 1])
    total += calculateDistance(route[len(route) - 1], route[0])
    return total


# *****************************************************************************
# Function to get the name of the file and access read permissions and collect
# the data that we need from the program specifications
# ******************************************************************************
def get_file_data(filename):
    with open(filename, "r") as inputFile:
        # loops through each line of file to gather data
        Cities = []  # this will hold the cities once we open the file
        # file is opened and Loop through each line in the file
        for line in inputFile:
            file_length = []
            # Split the line read at each white space
            lineNumbers = line.split()
            for num in lineNumbers:  # parse through each element that is in our input file
                file_length.append(int(num))
            Cities.append(City(file_length[0], file_length[1],
                               file_length[2]))  # add on the city that is read in and add this to the array of cities

    return Cities


# ******************************************************************************
# Function to get the name of the file and re name and append the .tours 
# ******************************************************************************
def output_file_rename(filename, tour, distance):
    # create the output file with the new name
    output_file = open(filename + ".tour", "w")
    print("\nOUTPUT FILE NAME: ", filename + ".tour")
    # write the length of the file plus 1 as specified in the program description
    output_file.write(str(distance) + '\n')
    # properly print
    for city in tour:
        output_file.write("{} {} {}\n".format(city.id, city.x, city.y))


# route is unvisited vertices (targets) v is current vertex (source)
def calc_closest_neighbor(source, targets):
    closest = None
    shortest_len = math.inf
    #print("\tSource: ", source)
    for target in targets:
        #print("\tTarget: ", target)
        #if target is not source:
        temp_distance = calculateDistance(source, target)
        if temp_distance < shortest_len:
            closest = target
            shortest_len = temp_distance
    return closest


def calc_neighbors(path):
    build_path = []
    current_city = path.pop(0)
    build_path.append(current_city)
    while path != []:
        node = calc_closest_neighbor(current_city, path)
        current_city = node
        path.remove(node)
        build_path.append(current_city)
    return build_path


def read_into_dict_list(filename):
    dict_from_file = []
    with open(filename) as f:
        for line in f:
            dict_entry = {}
            (id, x, y) = line.split()
            dict_entry['id'] = int(id)
            dict_entry['x'] = int(x)
            dict_entry['y'] = int(y)
            dict_entry['visited'] = False
            dict_from_file.append(dict_entry)
    return dict_from_file


def two_opt(path):
    flag = 1
    while flag:
        flag = 0
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                if j - i == 1:
                    continue  # changes nothing, skip then
                new_path = path[:]    # Creates a copy of path
                new_path[i:j] = path[j - 1:i - 1:-1]  # this is the 2-optSwap since j >= i we use -1
                if calculateTotalDistance(new_path) < calculateTotalDistance(path):
                    path = new_path    # change current path to best
                    flag = 1

    return path


# ******************************************************************************
# MAIN FUNCTION
# ******************************************************************************
start = time.time()  # get the starting time to be able to use later
# check and see if the number of command line arguments is less than 2 and if so re promt for a file name
# if len(sys.argv) < 2:
#     #get the file name from the user
#     filename = input("Please enter the file name\n")
#     #print out the name of the file
#     print("\nFILE NAME: ", filename)
#     #otherwise we have the file name and start the program
# else:
#     #style purpose
#     print("\n***********************************************************")
#     print("******** WELCOME TO THE TRAVELING SALESMAN PROBLEM ********")
#     print("***********************************************************")
#     #assign the proper comand line argument to the filename variable
#     filename = sys.argv[1]
#     #print out the file name
#     print("\nINPUT FILE NAME: ", filename)

# realign things below this comment when re implementing the above user input code

start = default_timer()

# get the file data
city_dict = read_into_dict_list("tsp_example_3.txt")

print("Initial Ordering of Cities...")
# for city in city_dict:
#     print(city)

print("\nNN Ordering of Cities...")
initial_calculation = calc_neighbors(city_dict)
# for vertex in initial_calculation:
#     print(vertex)

print("\n2OPT Ordering of Cities...")
two_opt_calc = two_opt(initial_calculation)
# for vertex in two_opt_calc:
#     print(vertex)

    # s = findTSPSolution(s, timeAvailable)
    # output_file_rename(filename, obj, calculateTotalDistance(obj))
end = default_timer()
print("Runtime: " + str(end - start) + " seconds.")
