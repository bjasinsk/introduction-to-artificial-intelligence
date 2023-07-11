import numpy
from autograd import grad, hessian
import autograd.numpy as anp
import matplotlib.pyplot as plt
import time
import random
import pandas as pd

def draw(pointsX, pointsY):
    range_x = 6
    distanceBetween = 0.1
    x_arr = anp.arange(-range_x, range_x, distanceBetween)
    y_arr = anp.arange(-range_x, range_x, distanceBetween)
    [X, Y]= anp.meshgrid(x_arr, y_arr)
    Z = anp.empty(X.shape)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = function(anp.array([X[i, j], Y[i, j]]))

    plt.contour(X, Y, Z, 35)

    plt.scatter(pointsX, pointsY)
    plt.title("Wykres przebiegu punktów")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.plot(pointsX[0], pointsY[0], color="red")
    plt.grid(linestyle="--")
    plt.show()

def function(x):
    return (x[0] * x[0] + x[1] - 11) ** 2 + (x[0] + x[1] * x[1] - 7) ** 2

def gradientMethod(x1 , x2, maxN, eps):
    pointsX = []
    pointsY = []
    start = time.time()
    x = anp.array([x1, x2], dtype='f')
    it = maxN

    f_grad = grad(function)

    for i in range(it):
        d = anp.array(f_grad(x))
        x -= eps * d
        pointsX.append(x[0])
        pointsY.append(x[1])

    end = time.time()
    operationTime = end - start
    minimum = function(x)
    result = [x, operationTime, minimum, pointsX, pointsY]
    return result

def newtonMethod(x1, x2, maxN, eps):
    pointsX = []
    pointsY = []
    start = time.time()
    x = anp.array([x1, x2], dtype='f')
    it = maxN
    f_grad = grad(function)
    f_hess = hessian(function)
    for i in range(it):
        gradient = f_grad(x)
        hess = f_hess(x)
        hess_inv = anp.linalg.inv(hess)
        d = anp.matmul(hess_inv, gradient)
        x -= eps * d
        pointsX.append(x[0])
        pointsY.append(x[1])

    end = time.time()
    operationTime = end - start
    minimum = function(x)
    result = [x, operationTime, minimum, pointsX, pointsY]
    return result

def generateDataTables(numberOfMeasurements, n, beta):

    measureResultsNewton = anp.array([])
    measureTimesNewton = anp.array([])

    measureResultsGradient = anp.array([])
    measureTimesGradient = anp.array([])

    for i in range(numberOfMeasurements):
        x1 = random.uniform(-5, 5)
        x2 = random.uniform(-5, 5)

        simpleMeasureNewton = newtonMethod(x1,  x2, n, beta)
        simpleMeasureGradient = gradientMethod(x1,  x2, n, beta)

        newtonMinimum = simpleMeasureNewton[2]
        newtonPoint = simpleMeasureNewton[0]
        newtonTime = simpleMeasureNewton[1]
        print("NewtonMethod: minimum: ",round(newtonMinimum,2), "współrzędne: ", [round(newtonPoint[0],2), round(newtonPoint[1],2)], "wylosowany punkt: ", [round(x1,2), round(x2,2)])
        draw(simpleMeasureNewton[3], simpleMeasureNewton[4])

        gradientMinimum = simpleMeasureGradient[2]
        gradientPoint = simpleMeasureGradient[0]
        gradientTime = simpleMeasureGradient[1]
        print("GradientMethod: minimum: ", round(gradientMinimum,2), "współrzędne: ", [round(gradientPoint[0],2), round(gradientPoint[1],2)], "wylosowany punkt: ", [round(x1,2), round(x2,2)])
        draw(simpleMeasureGradient[3], simpleMeasureGradient[4])

        measureResultsNewton = anp.append(measureResultsNewton, round(newtonMinimum, 2))
        measureTimesNewton = anp.append(measureTimesNewton, round(newtonTime,2))

        measureResultsGradient = anp.append(measureResultsGradient, round(gradientMinimum,2))
        measureTimesGradient = anp.append(measureTimesGradient, round(gradientTime,2))

    dataGradient = pd.DataFrame({'Minimum': measureResultsGradient, 'Czas - gradient': measureTimesGradient, 'iteracje':n, 'beta':beta})
    dataGradient.to_csv('reasultsOfMeasuresGradient.csv', index=False)

    dataNewton = pd.DataFrame({'Minimum': measureResultsNewton, 'Czas - Newton': measureTimesNewton, 'iteracje':n, 'beta':beta})
    dataNewton.to_csv('reasultsOfMeasuresNewton.csv', index=False)

    return


if __name__ == '__main__':

    numberOfMeasurements = 15
    n = 3000
    beta = 0.001

    generateDataTables(numberOfMeasurements, n, beta)

