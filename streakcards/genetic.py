import random
import copy
parent_file = open("parent_file", "r")

bets_file = open("bet_file", "w")

parent = []

child = []

for x in parent_file:
    parent = list(map(float, x.split()))

#print(parent)
for x in range(103):
    bets_file.write(str(parent[x]) + " "),
bets_file.write("\n")

for loop in range(15):
    idx = []
    x = 0
    while x != 10:
        rand_idx = random.randint(0,99)
        if rand_idx not in idx:
            idx.append(rand_idx)
            x += 1

    child = copy.deepcopy(parent)
    for x in idx:
        up_or_down = random.randint(0,1)
        if up_or_down == 0:
            if(child[x] - 20 <= 0):
                child[x] = 0
            else:
                child[x] -= 20
        else:
            if(child[x] + 20 >= 300):
                child[x] = 300
            else:
                child[x] += 20

    for x in range(103):
        bets_file.write(str(child[x]) + " "),
    bets_file.write("\n")
