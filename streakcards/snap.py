import numpy as np
import time
import math

trainingfile1 = open("trainingdata1.txt", "r")
trainingfile2 = open("trainingdata2.txt", "r")
trainingfile3 = open("trainingdata3.txt", "r")
trainingfile4 = open("trainingdata4.txt", "r")
trainingfile5 = open("trainingdata5.txt", "r")
trainingfile6 = open("trainingdata6.txt", "r")
trainingfile7 = open("trainingdata7.txt", "r")
trainingfile8 = open("trainingdata8.txt", "r")

probs0file = open("probs_0.txt", "r")

probs1file = open("probs_1.txt", "r")

probs2file = open("probs_2.txt", "r")

testingBanker = open("testingdataBanker.txt", "r")

testingPlayer = open("testingdataPlayer.txt", "r")

testingTie = open("testingdataTie.txt", "r")

best_bets_file = open("parent_file", "w")

bet_file = open("bet_file", "r")
trainingdata = []
trainingdataLabels = []
testingdata = []
testingdataLabels = []

bets = []
money = []



start = time.time()

probs0 = {}
data0 = probs0file.read()
probs0 = eval(data0)

total0 = len(probs0)



probs1 = {}
data1 = probs1file.read()
probs1 = eval(data1)


total1 = len(probs1)



probs2 = {}
data2 = probs2file.read()
probs2 = eval(data2)

total2 = len(probs2)

predict = 0

correct = 0
total = 0
for x in testingBanker:
    myarray = list(map(float, x.split()))
    label = myarray.pop()

    testingdata.append(myarray)
    testingdataLabels.append(label)

for x in testingPlayer:
    myarray = list(map(float, x.split()))
    label = myarray.pop()

    testingdata.append(myarray)
    testingdataLabels.append(label)

for x in testingTie:
    myarray = list(map(float, x.split()))
    label = myarray.pop()

    testingdata.append(myarray)
    testingdataLabels.append(label)


for x in bet_file:
    myarray = list(map(float, x.split()))
    bets.append(myarray)
    money.append(0)

for x,label in zip(testingdata, testingdataLabels):

    probs0val = 0
    probs1val = 0
    probs2val = 0

    try:
        probs0val = probs0[repr(x)]
    except KeyError:
        probs0val = 0

    try:
        probs1val = probs1[repr(x)]
    except KeyError:
        probs1val = 0

    try:
        probs2val = probs2[repr(x)]
    except KeyError:
        probs2val = 0
   #laplace smoothing
    player = float(float((probs0val + 1)/(total0))*(44.6/100.0))/float(float(probs0val + probs1val + probs2val + 3)/float(total0 + total1 + total2))
    banker = float(float((probs1val + 1)/(total1))*(45.9/100.0))/float(float(probs0val + probs1val + probs2val + 3)/float(total0 + total1 + total2))
    tie =    float(float((probs2val + 1)/(total2))*(9.5/100.0))/float(float(probs0val + probs1val + probs2val + 3)/float(total0 + total1 + total2))

    player *= 100.0
    banker *= 100.0
    tie *= 100.0

    player -= 44.6
    banker -= 45.9
    tie -= 9.5

    confidence = 0

    if max([player, banker, tie]) == player:
        predict = 0
        #get the difference betweent the 2
        player += 45.9
        confidence = math.floor(player)
    elif max([player, banker, tie]) == banker:
        predict = 1
        banker += 45.9
        confidence = math.floor(banker)
    elif max([player, banker, tie]) == tie:
        if max([player, banker]) == player:
            predict = 0
            player += 45.9
            confidence = math.floor(player)
        elif max([player,banker]) == banker:
            predict = 1
            banker += 45.9
            confidence = math.floor(banker)

    #print("Label: " + str(y) + " Predict: " + str(predict))
    if label == 2:
        for money_idx in range(16):
            money[money_idx] += 0

    elif label == predict:
        if label == 1:
            for money_idx in range(16):
                money[money_idx] += .95 * bets[money_idx][confidence]
        else:
            for money_idx in range(16):
                money[money_idx] += bets[money_idx][confidence]
    else:
        for money_idx in range(16):
            money[money_idx] -= bets[money_idx][confidence]
best_result = money[0]
best_idx = 0

for x in range(16):
    if money[x] > best_result:
        best_result = money[x]
        best_idx = x

print("Best Result: " + str(best_result))
print("Bets: " + repr(bets[best_idx]))

for x in range(103):
    best_bets_file.write(str(bets[best_idx][x]) + " "),
end = time.time()

print(end - start)
exit()

