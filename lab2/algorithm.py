import csv
import numpy as np
import random
import time
import pandas as pd

def init(n):
    initPopulation =[]
    citiesSet = list(range(0,30))

    for i in range(n):
        random.shuffle(citiesSet)
        perm = []
        perm = citiesSet[:]
        initPopulation.append(perm)
    return initPopulation

def mark(indyvidual):
    fullRoad = 0
    for i in range(0, len(indyvidual) - 1):
        fullRoad += matrix[indyvidual[i]][indyvidual[i+1]]
    fullRoad += matrix[indyvidual[-1]][indyvidual[0]]
    return fullRoad

def markPopulation(populationList):
    result = []
    for i in range(0, len(populationList) - 1):
        markedIndyvidual = mark(populationList[i])
        result.append([markedIndyvidual, populationList[i]])

    return result

def tournamentSelection(Pt):
    Tt =[]
    for i in range(len(Pt)):
        i1, i2 = random.sample(Pt, 2)
        if i1[0] < i2[0]:
            Tt.append(i1)
        else:
            Tt.append(i2)

    return Tt

def mutation(Tt, n, p):
    Ot = Tt[:]
    for i in range(n):
        elementToMutate = random.randint(0,len(Tt) - 1)
        indexes = list(range(0,30))
        index1, index2 = random.sample(indexes, 2)
        if random.random() < p:
            Ot[elementToMutate][1][index1], Ot[elementToMutate][1][index2] = Ot[elementToMutate][1][index2], Ot[elementToMutate][1][index1]
            Ot[elementToMutate][0] = mark(Ot[elementToMutate][1])
    return Ot

def findBest(population):
    population_sorted = population.copy()
    population_sorted.sort(key=lambda population: population[0])
    return population_sorted[0].copy()

if __name__ == '__main__':

    with open('data.csv', 'r') as file:
        csvreader = csv.reader(file)
        matrix = np.loadtxt('data.csv', delimiter=',')

    bestCombinations = np.array([])
    bestResults = np.array([])
    times = np.array([])

    iterations = 400
    mutationParameter = 0.3
    sizeOfPopulation = 240


    start = time.time()
    combinations = init(sizeOfPopulation)
    Pt = markPopulation(combinations)
    end = time.time()
    times = np.append(times, round(end - start,2))
    best = findBest(Pt)
    bestCombinations = np.append(bestCombinations, best[1])
    bestResults = np.append(bestResults, best[0])
    t = 0
    while t != iterations:
        start = time.time()
        Tt = tournamentSelection(Pt)
        Ot = mutation(Tt, sizeOfPopulation, mutationParameter)
        localBest = None
        localBest = findBest(Ot)
        bestCombinations = np.append(bestCombinations, localBest[1])
        bestResults = np.append(bestResults, localBest[0])
        if localBest[0] < best[0]:
            best = localBest.copy()
        end = time.time()
        times = np.append(times, round(end - start, 2))
        Pt = Ot
        t += 1

    resultsOfMeasurements = pd.DataFrame({'The shortest path': bestResults, 'Time of single iteration': times, 'mutation parameter': mutationParameter})
    resultsOfMeasurements.to_csv('resultsOfMeasurements.csv', index=False)

    minimum = np.min(bestResults)
    maximum = np.max(bestResults)
    average = np.mean(bestResults)
    standardDeviation = np.std(bestResults)
    print("minimum of results: ", round(minimum, 2))
    print("maximum of results: ", round(maximum, 2))
    print("average of results: ", round(average, 2))
    print("std of results: ", round(standardDeviation, 2))

