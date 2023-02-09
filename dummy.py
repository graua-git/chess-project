directions = [2, -2, 1, -1]
permutations = []

for i in range(len(directions)):
    for j in range(len(directions)):
       if abs(directions[i]) != abs(directions[j]):
            permutations.append((directions[i], directions[j]))

print(len(permutations), permutations)
