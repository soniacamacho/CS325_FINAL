import itertools


def n_size_subsets(full_set, n):
    return [set(i) for i in itertools.combinations(full_set, n)]


s = {1, 2, 3, 4, 5}
n = 3

print(n_size_subsets(s, n))
