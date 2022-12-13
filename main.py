import re
import random
import math
import matplotlib.pyplot as plt




class Vector():

    def __init__(self, x: int, y: int):
        self.xPos = x
        self.yPos = y

    def changePos(self, x: int, y: int):
        self.xPos = x
        self.yPos = y

    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos

# key: Kommun_code
# 0: Year
# 1: Kommun_name
# 2: Revenue
# 3: Employee
# 4: Population
# 5: Population_University
# 6: Percent_University
# 7: Productivity
# 8: SalesIndex
# 9: Infrast
# 10: Border
allPoints = {}
k = 0

def hasNumbers(inputStr: str):
    return bool(re.search(r"\d", inputStr))

def formatData():
    global allPoints
    with open("data.txt", "r") as f:
        f.readline() #Removes first unecessary line
        
        while True:
            line = f.readline()
            if not line:
                break
            else:
                elements = line.split()
                if not hasNumbers(elements[3]):
                    elements[2] = elements[2] + " " + elements[3]
                    del elements[3]

                kommunCode = ""
                for i in range(len(elements)):
                    if(i == 0):
                        kommunCode = elements[0]
                        allPoints[kommunCode] = []
                    else:
                        allPoints[kommunCode].append(elements[i])


def getMax(allPoints ,index: int) -> int:
    currentMax = 0
    for key in allPoints:
        value = int(allPoints[key][index])

        if value > currentMax:
            currentMax = value
    
    return currentMax

def getMin(allPoints ,index: int) -> int:
    currentMin = 999999999
    for key in allPoints:
        value = int(allPoints[key][index])

        if value < currentMin:
            currentMin = value

    return currentMin


def setK(kVal: int):
    global k
    k = kVal

def printCentroids(centroids):
    for centroid in centroids:
        print("X: " + str(centroid.getX()) + ", Y: " + str(centroid.getY()))


def formatClusters(index1: int, index2: int):
    maxIndex1, minIndex1 = getMax(allPoints ,index1), getMin(allPoints, index1)
    maxIndex2, minIndex2 = getMax(allPoints ,index2), getMin(allPoints, index2)

    centroids = [Vector(random.randrange(minIndex1, maxIndex1), random.randrange(minIndex2, maxIndex2)) for _ in range(k)]
    
    print("Before: ")
    printCentroids(centroids)

    clusters = updateClusters(allPoints, centroids, index1, index2)
    updateCentroids(centroids, clusters)

    print("After: ")
    printCentroids(centroids)

    # Assigna datapunkter till närmsta centroid
    # Beräkna nytt medelvärde för centroider
    # Gör om tills centroiderna har konvergerat
    
    index = 0
    prevCentroids = []
    while True:

        clusters = updateClusters(allPoints, centroids, index1, index2)
        updateCentroids(centroids, clusters)

        if hasConverged(prevCentroids, centroids):
            break
        else:
            printCentroids(centroids)
            prevCentroids = centroids

    print("Finished centroids: ")
    printCentroids(centroids)



# Creates a new cluster 
def updateClusters(allPoints, centroids, index1, index2):
    newClusters = [
        [] for _ in centroids
    ]

    for key in allPoints:
        dataX = int(allPoints[key][index1])
        dataY = int(allPoints[key][index2])

        currentMin = 999999
        index = 0
        for i in range(len(centroids)):
            centroidX = centroids[i].getX()
            centroidY = centroids[i].getY()

            eucDist = getEuclideanDist(dataX, dataY, centroidX, centroidY)
            if eucDist < currentMin:
                currentMin = eucDist
                index = i


        # When finished comparing value insert with correct centroid
        newClusters[index].append(Vector(dataX, dataY))

    return newClusters



def updateCentroids(centroids, newClusters):
    #Update the positions of the centroids based on the new clusters.
    #
    #Args:
    #    centroids (List[Object]): The list of centroids to update.
    #    newClusters (List[List[Object]]): The new clusters of objects.

    # Loop through the centroids
    for i in range(len(centroids)):
        # Initialize the sums of the x and y coordinates
        sumX = 0
        sumY = 0

        # Loop through the elements in the cluster
        for elements in newClusters[i]:
            # Sum the x and y coordinates of the elements
            sumX = sumX + elements.getX()
            sumY = sumY + elements.getY()

        # Calculate the average x and y coordinates
        try:
            avgX = sumX/len(newClusters[i])
            avgY = sumY/len(newClusters[i])
            # Update the position of the centroid
            centroids[i].changePos(avgX, avgY)
        except ZeroDivisionError:
            # Handle the case where the cluster is empty
            print(newClusters)
            print("Division by zero in updateCentroids()")



def hasConverged(prevCentroids, currentCentroids) -> bool:
    # Initialize the counter variable
    counter = 0

    # Loop through the current and previous centroids
    for c1 in currentCentroids:
        for c2 in prevCentroids:
            # Check if the centroids have not moved significantly
            if (c1.getX() - c2.getX() < 100) and (c1.getY() - c2.getY() < 100):
                # Increment the counter if they have not moved
                counter = counter + 1

    # Check if all centroids have not moved significantly
    if counter == len(currentCentroids):
        # Return True if they have not moved
        return True

    # Return False if any centroid has moved significantly
    return False


def getEuclideanDist(x1, y1, x2, y2) -> float:
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    
if __name__ == "__main__":
    formatData()
    print(allPoints)
    setK(3)
    #Calculating k-mean for revenue and population
    formatClusters(2, 4)


