import numpy as np
import csv

np.random.seed(2222)

matrix = np.random.randint(1, 20, size=(30, 30))
for i in range(30):
    for j in range(i+1, 30):
        matrix[j, i] = matrix[i, j]

with open('data.csv', 'w') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(matrix)

