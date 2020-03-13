#*****************************************************************************
# CS 325 FINAL PROJECT TRAVELING SALESMAN PROBLEM
# BY : SONIA CAMACHO OWEN MARKLEY ANJALI Vasisht
#*****************************************************************************
import math
import sys
import time
from timeit import default_timer

class City  : 
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.visited = False 



# *****************************************************************************
# Function to get the distance between two points 
# ******************************************************************************
def calculateDistance(city1, city2):
    x_distance = abs(city1['x'] - city2['x'])
    y_distance = abs(city1['y'] - city2['y'])
    return int(round(math.sqrt(x_distance * x_distance + y_distance * y_distance)))
#*****************************************************************************
# Function to get the total distance, this was outlined in the program sepcification
#******************************************************************************   
def calculateTotalDistance(path):
    total = 0
    last_stop = path[0]
    for i, stop in enumerate(path):
        if i != 0:
            total += calculateDistance(last_stop, stop)
        last_stop = stop
    total += calculateDistance(last_stop, path[0])
    return total
#*****************************************************************************
# Function to get the name of the file and access read permissions and collect
# the data that we need from the program specifications
#******************************************************************************
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
#******************************************************************************
# Function to get the name of the file and re name and append the .tours 
#******************************************************************************
def output_file_rename(filename, tour, distance):
    #create the output file with the new name 
    output_file =  open (filename + ".tour", "w") 
    #print("\nOUTPUT FILE NAME: ", filename + ".tour") 
    #write the length of the file plus 1 as specified in the program description
    output_file.write(str(distance) + '\n')
    #properly print
    for city in tour:
        output_file.write("{} {} {}\n".format(city['id'], city['x'], city['y']))  
        
#******************************************************************************
# Function to get the closest neighbor 
#******************************************************************************
def calc_closest_neighbor(source, targets):
    closest = None
    shortest_len = math.inf
    for target in targets:
        if target is not source:
            temp_distance = calculateDistance(source, target)
            if temp_distance < shortest_len:
                closest = target
                shortest_len = temp_distance
    return closest
#******************************************************************************
# Function to get the nearest neighbors following the pseudo code 
# sourced from https://www.slideshare.net/AkshayKamble24/travelling-salesman-problemtsp
# Home_City = Visited = Current_city
# While(!visitedAll_City) 
# Node = Find_Shortest_distance(Current_node)
# Add_Node (Node) 
# Current_node = Node 
# Result = All_node + Home_City[0][last_Visit_Node] 
# return Final_result= Result
#******************************************************************************
def calc_neighbors(path):
    build_path = []  # setting the empty path that will build the new path will all the cities
    current_city = path.pop(0)  # get our current city that were at
    build_path.append(current_city)  # all this city to our new path were building
    while path != []:  # while the path is not empty
        node = calc_closest_neighbor(current_city, path)  # get the closest neighbor
        current_city = node  # set the new current city to be the node
        path.remove(node)  # pop that node off our OG path
        build_path.append(current_city)  # and add it into the new path we built
    return build_path  # return our new path we built

#******************************************************************************
# Function to perform the 2-opt stuff
#******************************************************************************
def two_opt_fast(path):
    #print(path)
    flag = 1
    while flag:
        flag = 0
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                time_rem = 300 - (time.time() - start)
                if time_rem < 2.0:
                    return path
                if j - i == 1:
                    continue
                #print("here")
                new_path = path[:]
                #print(new_path)
                new_path[i:j] = path[j-1:i-1:-1]
                #print(new_path)
                if cost_change(new_path[i - 1], new_path[i], new_path[j - 1], new_path[j]) < 0:
                    path = new_path
                    flag = 1
    return path

#******************************************************************************
# Function to perform the cost difference 
#******************************************************************************
def cost_change(v1, v2, v3, v4):
    #print("calcing...", v1, v2, v3, v4)
    return (calculateDistance(v1, v2) + calculateDistance(v3, v4)) - (calculateDistance(v1, v3) + calculateDistance(v2, v4))

#******************************************************************************
#MAIN FUNCTION
#******************************************************************************
start = time.time() #get the starting time to be able to use later 
#check and see if the number of command line arguments is less than 2 and if so re promt for a file name 
if len(sys.argv) < 2:
    #get the file name from the user
    filename = input("Please enter the file name\n") 
    #print out the name of the file 
    #print("\nFILE NAME: ", filename)  

#otherwise we have the file name and start the program
#style purpose
print("\n***********************************************************")
print("******** WELCOME TO THE TRAVELING SALESMAN PROBLEM ********")
print("***********************************************************")
#assign the proper comand line argument to the filename variable 
filename = sys.argv[1]
#print out the file name 
#print("\nINPUT FILE NAME: ", filename) 
#start = default_timer()
#get the file data
path = read_into_dict_list(filename)

vecinos = calc_neighbors(path)
#print("Finished vecinos")
time_available = str(300 - (time.time() - start))
#print("Time Available: ", time_available)
two_opted = two_opt_fast(vecinos)
calculated_total_d = calculateTotalDistance(two_opted)
output_file_rename(filename, two_opted, calculateTotalDistance(two_opted))

end = time.time()#default_timer()
print("Runtime: " + str(end - start) + " seconds.")
#optimal_length = 1573084
#print("Accuracy: ", "(", calculated_total_d, ")/(", optimal_length, ")", (calculated_total_d * 1.0 / optimal_length * 1.0))


'''
#get the file data
path = read_into_dict_list(filename)

vecinos = calc_neighbors(path)
print("DONE WITH VECINOS")
#re update since vecinos changes it 
path = read_into_dict_list(filename)

path = two_opt(vecinos)

#s = findTSPSolution(s, timeAvailable)
output_file_rename(filename, path, calculateTotalDistance(path))
end = default_timer()
print("Runtime: " + str(end-start) + " seconds.")
'''
