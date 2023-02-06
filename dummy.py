moves = [2, -2, 1, -1]
permutations = []
for i in range(len(moves)):
    for j in range(len(moves)):
        if abs(moves[i]) != abs(moves[j]):
            permutations.append((moves[i], moves[j]))

print(permutations)
print(len(permutations))