import math
import pandas as pd
from Tree import Tree

def frequencyDictionary(u):
    yValues = {}
    for x, y in u:
        if y not in yValues:
            yValues[y] = 1
        else:
            yValues[y] += 1
    return yValues

def entropy(u):
    yValues = frequencyDictionary(u)
    result = 0.0
    n = len(u)

    for classValue in yValues:
        v = yValues[classValue] / n
        result -= v * math.log2(v)
    return result

#W Twoim przypadku zbiór Y to zbiór klas, czyli klasa, którą chcesz przewidzieć.
#Zbiór D to zbiór atrybutów wejściowych, które mają być użyte do klasyfikacji.
#Zbiór U to zbiór par uczących, czyli zestaw danych, które będziesz używać do uczenia modelu.
#Każda para ucząca składa się z wektora cech (atrybutów wejściowych) oraz odpowiadającej mu klasy (wartości klasowej).
#Algorytm ID3 wykorzystuje ten zbiór danych uczących, aby stworzyć drzewo decyzyjne, które może być wykorzystane do klasyfikacji nowych danych.

def entropySubsets(u, d):

    frequencyAttributes = {}
    for x, y in u:
        if x[d] not in frequencyAttributes:
            frequencyAttributes[x[d]] = [(x,y)]
        else:
            frequencyAttributes[x[d]].append((x,y))

    result = 0.0
    n = len(u)

    for v in frequencyAttributes.values():
        simpleCalculation = len(v)/n
        result += simpleCalculation * entropy(v)

    return result

def infGain(u, d):
    return entropy(u) - entropySubsets(u, d)

def leafMostFrequentClass(matrix, u):
    yValues = frequencyDictionary(u)

    maxValue = max(yValues.values())
    for y in yValues:
        if yValues[y] == maxValue:
            return leafWithClass(matrix, y)


def leafWithClass(matrix, y):
    selectedData = []
    for row in matrix:
        if row[-1] == y:
            selectedData.append(row)
    return selectedData


# Y  set of classes which we try to find
# D set of attributes, we use them to define nodes in decision tree
# U set of pairs which teach an algorithm, U can't be empty
def id3(matrix, y, d, u):
    yCount = frequencyDictionary(u)

    for ySimple in y:
        if ySimple in yCount and yCount[ySimple] == len(u):
            return leafWithClass(matrix, ySimple)

    if len(d) == 0:
        return leafMostFrequentClass(matrix, u)

    maxGain = float('-inf')
    maxAttribute = None
    for simpleD in d:
        gain = infGain(u, simpleD)
        if gain > maxGain:
            maxGain = gain
            maxAttribute = simpleD

    dToDivide = maxAttribute

    Uj = {}
    for x, y in u:
        if x[d] not in Uj:
            Uj[x[d]] = [(x, y)]
        else:
            Uj[x[d]].append((x, y))

    subTrees = {}
    for dj, UjSet in Uj.items():
        subTrees[dj] = id3(matrix, y, d - {dToDivide}, UjSet)

    return Tree(d, subTrees)

if __name__ == '__main__':
    Y = ["not_recom", "recommend", "very_recom", "priority", "spec_prior"]
    D = ["parents, has_nurs, form, children, housing, finance, social, health"]

    df = pd.read_csv('nursery.data')
    matrix = df.values


    print(matrix)
