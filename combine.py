from itertools import combinations

s = [1,2,3,4]

results = {}

for i in range(2, len(s) + 1):
    results[i] = list(combinations(s, i))

print(results)


