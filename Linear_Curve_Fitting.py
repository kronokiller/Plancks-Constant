import os

def getData(path):
    file = open(path)
    dataPoints = []
    for line in file:
        dataPoints.append((line.split(' ')[0], line.split(' ')[1][:-1]))

    return dataPoints

def getLines(dataPoints):
    line = []
    x = 0
    for i in range(len(dataPoints)):
        if float(dataPoints[0][0]) >= x:
            x = float(dataPoints[0][0])
            line.append(dataPoints.pop(0))
        else:
            return [line] + getLines(dataPoints)
    return [line]

def linearRegression(dataPoints):
    weightedSumX = sum([point[0] / point[1][1] ** 2 for point in dataPoints])
    weightedSumY = sum([point[1][0] / point[1][1] ** 2 for point in dataPoints])
    weightedSumXY = sum([point[0] * point[1][0] / point[1][1] ** 2 for point in dataPoints])
    sumOfWeights = sum([1 / point[1][1] ** 2 for point in dataPoints])
    weightedSumXSquared = sum([point[0] ** 2 / point[1][1] ** 2 for point in dataPoints])

    slope = (weightedSumX * weightedSumY - weightedSumXY * sumOfWeights) / (weightedSumX ** 2 - weightedSumXSquared * sumOfWeights)
    intercept = (weightedSumXY - slope * weightedSumXSquared) / weightedSumX
    slopeErr = (sumOfWeights / (weightedSumXSquared * sumOfWeights - weightedSumX ** 2)) ** (1 / 2)
    interceptErr = (weightedSumXSquared / (weightedSumXSquared * sumOfWeights - weightedSumX ** 2)) ** (1 / 2)

    return (intercept, slope, interceptErr, slopeErr)

def standardDeviation(list):
    n = len(list)
    xBar = sum([float(dataPoint) for dataPoint in list]) / n
    Sx = (sum([(float(value) - xBar) ** 2 for value in list]) / (n - 1)) ** (1 / 2)
    return (xBar, Sx)

def getZero(line, method):
    previousPoint = (0, 0)
    for point in line:
        if method == 0 and (float(point[1]) - float(previousPoint[1])) / (float(point[0]) - float(previousPoint[0])) > - 3 * 10 ** (-10) and float(previousPoint[1]) < - 1 * 10 ** (-10) and previousPoint != (0, 0):
            return previousPoint[0]
        if method == 1 and (float(point[1])) < 10 ** (-9):
            return previousPoint[0]
        previousPoint = point

def trial(path, method, buffer):
    xInts = []
    for line in getLines(getData(path)):
        xInts.append(getZero(line, 0))
    print(' ' * buffer + path[:-8] + 'nm|', standardDeviation(xInts)[0], '+-', standardDeviation(xInts)[1])
    return standardDeviation(xInts)

def f(wavelength):
    return 299792458 / wavelength

def h(slope):
    return slope * e

os.chdir(os.path.dirname(__file__))

nm = 10 ** (-9)
e = 1.602 * 10 ** (-19)
c = 299792458

method = 0
points = []

print('\nWavelength| Stopping Potential (V)')
print('=' * 53)
points.append((f(435.8 * nm), trial('435.8 data.txt', method, 2)))
points.append((f(546 * nm), trial('546 data.txt', method, 4)))
points.append((f(577 * nm), trial('577 data.txt', method, 4)))

info = linearRegression(points)
print('\ny = mx + b')
print('m =', str(info[1]), '+-', info[3])
print('b =', str(info[0]), '+-', info[2])
print('\nh = m * charge of an electron')
print('h =', h(info[1]), '+-', h(info[3]), '\n')


