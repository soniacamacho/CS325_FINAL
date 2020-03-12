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
#*****************************************************************************
# Function to get the distance between two points 
#******************************************************************************          
def calculateDistance(city1, city2):
    x_distance = abs(city1.x - city2.x)
    y_distance = abs(city1.y - city2.y) 
    return int(round(math.sqrt(x_distance * x_distance + y_distance * y_distance))) 
#*****************************************************************************
# Function to get the total distance, this was outlined in the program sepcification
#******************************************************************************   
def calculateTotalDistance(path):
    total = 0
    for idx in range(0, len(path)-1):
        total += calculateDistance(path[idx], path[idx+1])
    total += calculateDistance(path[len(path)-1], path[0])   
    return total
#*****************************************************************************
# Function to get the name of the file and access read permissions and collect
# the data that we need from the program specifications
#******************************************************************************
def get_file_data(filename):
    with open (filename, "r") as inputFile:
        #loops through each line of file to gather data
        Cities = []#this will hold the cities once we open the file 
        # file is opened and Loop through each line in the file
        for line in inputFile:
            file_length = []
            # Split the line read at each white space
            lineNumbers = line.split()
            for num in lineNumbers: #parse through each element that is in our input file 
                file_length.append(int(num))
            Cities.append(City(file_length[0], file_length[1], file_length[2])) # add on the city that is read in and add this to the array of cities 

    return Cities
#******************************************************************************
# Function to get the name of the file and re name and append the .tours 
#******************************************************************************
def output_file_rename(filename, tour, distance):
    #create the output file with the new name 
    output_file =  open (filename + ".tour", "w") 
    print("\nOUTPUT FILE NAME: ", filename + ".tour") 
    #write the length of the file plus 1 as specified in the program description
    output_file.write(str(distance) + '\n')
    #properly print
    for city in tour:
        output_file.write("{} {} {}\n".format(city.id, city.x, city.y))

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
    build_path = []
    current_city = path.pop(0)
    build_path.append(current_city)
    while path != []:
        node = find_shortest_distance(current_city, path)
        current_city = node
        path.remove(node)
        build_path.append(current_city)        
    return build_path

#******************************************************************************
# function to get the actual solution
#******************************************************************************

#******************************************************************************
#MAIN FUNCTION
#******************************************************************************
start = time.time() #get the starting time to be able to use later 
#check and see if the number of command line arguments is less than 2 and if so re promt for a file name 
if len(sys.argv) < 2:
    #get the file name from the user
    filename = input("Please enter the file name\n") 
    #print out the name of the file 
    print("\nFILE NAME: ", filename)  

#otherwise we have the file name and start the program
#style purpose
print("\n***********************************************************")
print("******** WELCOME TO THE TRAVELING SALESMAN PROBLEM ********")
print("***********************************************************")
#assign the proper comand line argument to the filename variable 
filename = sys.argv[1]
#print out the file name 
print("\nINPUT FILE NAME: ", filename) 
start = default_timer()

#get the file data
path = get_file_data(filename)

vecinos = calc_neighbors(path)

#path = sol(path)

#s = findTSPSolution(s, timeAvailable)
output_file_rename(filename, path, calculateTotalDistance(path))
end = default_timer()
print("Runtime: " + str(end-start) + " seconds.")
