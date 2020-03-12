# *****************************************************************************
# CS 325 FINAL PROJECT TRAVELING SALESMAN PROBLEM
# BY : SONIA CAMACHO OWEN MARKLEY ANJALI Vasisht
# *****************************************************************************
import itertools
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
        return f'{self.id} {self.x} {self.y}'


class SubPath:
    cost = -1
    parent = None

    def __init__(self, id, subset):
        self.id = id
        self.subset = subset

    def __str__(self):
        return f'[ {self.id} {self.subset} ] = Cost: {self.cost} Parent: {self.parent}'


# *****************************************************************************
# Function to get the distance between two points 
# ******************************************************************************
def calculateDistance(city1, city2):
    x_distance = abs(city1.x - city2.x)
    y_distance = abs(city1.y - city2.y)
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
    # completed list of vertices is stored here in coordinate form
    with open(filename) as f:  # size n
        coordinates = [tuple(map(int, i.split(' '))) for i in f]
    cities = [City(coordinate_pair[0], coordinate_pair[1], coordinate_pair[2]) for coordinate_pair in coordinates]

    return cities


def create_dist_matrix(cities):
    distance_matrix = [[calculateDistance(source_city, target_city) for target_city in cities] for source_city in
                       cities]

    return distance_matrix


def n_size_subsets(full_set, n):
    return [set(i) for i in itertools.combinations(full_set, n)]


# ******************************************************************************
# Function to get the name of the file and re name and append the .tours 
# ******************************************************************************
def output_file_rename(filename, tour, distance):
    # create the output file with the new name
    output_file = open(filename + ".tour", "w")
    # write the length of the file plus 1 as specified in the program description
    output_file.write(str(distance) + '\n')
    # properly print
    for city in tour:
        output_file.write("%d\n" % city.id)


# ******************************************************************************
# MAIN FUNCTION
# ******************************************************************************
"""
start = time.time()  # get the starting time to be able to use later
# check and see if the number of command line arguments is less than 2 and if so re promt for a file name
if len(sys.argv) < 2:
    # get the file name from the user
    filename = input("Please enter the file name\n")
    # print out the name of the file
    print("\nFILE NAME: ", filename)
# otherwise we have the file name and start the program
else:
    # style purpose
    print("\n***********************************************************")
    print("******** WELCOME TO THE TRAVELING SALESMAN PROBLEM ********")
    print("***********************************************************")
    # assign the proper comand line argument to the filename variable
    filename = sys.argv[1]
    # print out the file name
    print("\nFILE NAME: ", filename)
    start = default_timer()
"""
# get the file data
city_list = get_file_data("tsp_example_1.txt")

# s = findTSPSolution(s, timeAvailable)
# output_file_rename(filename, obj, calculateTotalDistance(obj))
# end = default_timer()
# print("Runtime: " + str(end - start) + " seconds.")
d_matrix = create_dist_matrix(city_list)
print("---DISTANCE MATRIX---")
for i, row in enumerate(d_matrix):
    print(i, row)
print()

city_name_set = {city.id for city in city_list}
city_name_set.remove(city_list[0].id)

# city_name_subsets = []
# for i in range(1, len(city_name_set)):
#     temp = n_size_subsets(city_name_set, i)
#     city_name_subsets.append(temp)
# #print("CITY ID SUBSETS: ", city_name_subsets)

stored_solutions = [[] for k in range(len(city_name_set))]
# print("STORED EFFICIENT SUBPATHS: ", stored_solutions)

stored_solutions[0] = [SubPath(city.id, set()) for i, city in enumerate(city_list) if i != 0]
for i, stored_path in enumerate(stored_solutions[0]):
    stored_path.parent = 0
    stored_path.cost = d_matrix[0][i + 1]

# for stored_path in stored_solutions[0]:
#    print(stored_path)

print(len(city_name_set))
print()
for i in range(0, len(city_name_set)-1):
    nset = n_size_subsets(city_name_set, i+1)
    for subset in nset:
        for vertex in city_name_set - subset:
            a = SubPath(vertex, subset)
            #print("\t[", vertex, subset, "]")
            costs_to_compare = []
            for j, set_vertex in enumerate(subset):
                temp_dist = d_matrix[set_vertex][vertex]#calculateDistance(city_list[set_vertex], city_list[vertex])
                #print("\t\tDistance ", vertex, "to ", set_vertex, ": ", temp_dist)
                subtracted_set = subset - {set_vertex}
                #print("\t\tSubtractedSet: ", subtracted_set)
                for retrieved_sol in stored_solutions[i]:
                    if (retrieved_sol.id == set_vertex) and (subtracted_set == retrieved_sol.subset):
                        #print("\t\t", retrieved_sol)
                        costs_to_compare.append((set_vertex, temp_dist + retrieved_sol.cost))
            #print("\t", costs_to_compare)
            opt_path = min(costs_to_compare, key=lambda x: x[1])
            a.parent = opt_path[0]
            a.cost = opt_path[1]
            print(a)
            stored_solutions[i + 1].append(a)


# for i, size_sorted_sub_list in enumerate(city_name_subsets):
#     print(i, size_sorted_sub_list)
#     #print("Subsets of Size: ", i + 1)
#     for subset in size_sorted_sub_list:
#         for vertex in city_name_set - subset:
#             a = SubPath(vertex, subset)
#             #print("\t[", vertex, subset, "]")
#             costs_to_compare = []
#             for j, set_vertex in enumerate(subset):
#                 temp_dist = d_matrix[set_vertex][vertex]#calculateDistance(city_list[set_vertex], city_list[vertex])
#                 #print("\t\tDistance ", vertex, "to ", set_vertex, ": ", temp_dist)
#                 subtracted_set = subset - {set_vertex}
#                 #print("\t\tSubtractedSet: ", subtracted_set)
#                 for retrieved_sol in stored_solutions[i]:
#                     if (retrieved_sol.id == set_vertex) and (subtracted_set == retrieved_sol.subset):
#                         #print("\t\t", retrieved_sol)
#                         costs_to_compare.append((set_vertex, temp_dist + retrieved_sol.cost))
#             #print("\t", costs_to_compare)
#             opt_path = min(costs_to_compare, key=lambda x: x[1])
#             a.parent = opt_path[0]
#             a.cost = opt_path[1]
#             #print(a)
#             stored_solutions[i + 1].append(a)

# print("\nSTORED EFFICIENT SUBPATHS: ")
# for solution_of_nset in stored_solutions:
#     for stored_path in solution_of_nset:
#         print(stored_path)

fp_costs_to_compare = []
final_sub_path = SubPath(0, city_name_set)

for vertex in city_name_set:
    dist = d_matrix[vertex][0]
    subtracted_set = city_name_set - {vertex}
    subtracted_set_cost = -1
    for size_3_solution in stored_solutions[2]:
        if size_3_solution.subset == subtracted_set:
            subtracted_set_cost = size_3_solution.cost
    fp_costs_to_compare.append((vertex, dist + subtracted_set_cost))
    opt_path = min(fp_costs_to_compare, key=lambda x: x[1])
    final_sub_path.cost = opt_path[1]
    final_sub_path.parent = opt_path[0]

# print(final_sub_path)

temp_city_set = city_name_set
stops_in_order = [0]
tempSubPath = final_sub_path
counter = len(stored_solutions) - 1
while len(temp_city_set) > 0:
    backtracking_v = tempSubPath.parent
    temp_city_set = tempSubPath.subset - {backtracking_v}
    for sol in stored_solutions[counter]:
        if(sol.id == backtracking_v) and (sol.subset == temp_city_set):
            tempSubPath = sol
    stops_in_order.append(backtracking_v)
    counter = counter - 1
stops_in_order.append(final_sub_path.id)

print()
print("Results:")
print("\tTour Length: ", final_sub_path.cost)
print("\tTour Stops in Order:", stops_in_order)
#print(len(city_name_subsets))
