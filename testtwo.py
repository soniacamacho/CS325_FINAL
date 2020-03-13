import math
import sys
import time
from timeit import default_timer

def calculateDistance(city1, city2):
	x_distance = abs(city1['x'] - city2['x'])
	y_distance = abs(city1['y'] - city2['y'])
	return int(round(math.sqrt(x_distance * x_distance + y_distance * y_distance)))

def calculateTotalDistance(path):
	total = 0
	last_stop = path[0]
	for i, stop in enumerate(path):
		if i != 0:
			total += calculateDistance(last_stop, stop)
		last_stop = stop
	total += calculateDistance(last_stop, path[0])
	return total

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

# def two_opt(path):
# 	optimised = path
# 	flag = 1
# 	while flag:
# 		flag = 0
# 		for i in range(1, len(path) - 2):
# 			for j in range(i + 1, len(path)):
# 				if j - i == 1:
# 					continue  # changes nothing, skip then
# 				# new_path = path[:]    # Creates a copy of path
# 				# this is the 2-optSwap since j >= i we use -1
# 				if cost_change(optimised[i - 1], optimised[i], optimised[j - 1], optimised[j]) < 0:
# 					optimised[i:j] = optimised[j - 1:i - 1:-1]
# 					# path = new_path    # change current path to best
# 				flag = 1
# 		path = optimised
# 	return optimised

# def two_opt(path):
#     flag = 1
#     while flag:
#         flag = 0
#         for i in range(1, len(path) - 2):
#             for j in range(i + 1, len(path)):
#                 if j - i == 1:
#                     continue  # changes nothing, skip then
#                 new_path = path[:]    # Creates a copy of path
#                 new_path[i:j] = path[j - 1:i - 1:-1]  # this is the 2-optSwap since j >= i we use -1
#                 if calculateTotalDistance(new_path) < calculateTotalDistance(path):
#                     path = new_path    # change current path to best
#                     flag = 1

#     return path

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


def cost_change(v1, v2, v3, v4):
	#print("calcing...", v1, v2, v3, v4)
	return (calculateDistance(v1, v2) + calculateDistance(v3, v4)) - (calculateDistance(v1, v3) + calculateDistance(v2, v4))

# ===================================================================================================================================
start = time.time()
#start = default_timer()

path = read_into_dict_list("test-input-7.txt")
#print(path)
vecinos = calc_neighbors(path)
print("Finished vecinos")
time_available = str(300 - (time.time() - start))
print("Time Available: ", time_available)
two_opted = two_opt_fast(vecinos)

calculated_total_d = calculateTotalDistance(two_opted)
end = time.time()#default_timer()
print("Runtime: " + str(end - start) + " seconds.")
optimal_length = 1573084
print("Accuracy: ", "(", calculated_total_d, ")/(", optimal_length, ")", (calculated_total_d * 1.0 / optimal_length * 1.0))