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

    def setX(self, x: int):
        self.xPos = x

    def setY(self, y: int):
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


def getMaxPoints(allPoints ,index: int) -> int:
    currentMax = 0
    for key in allPoints:
        value = int(allPoints[key][index])

        if value > currentMax:
            currentMax = value
    
    return currentMax

def getMinPoints(allPoints ,index: int) -> int:
    currentMin = float('inf')
    for key in allPoints:
        value = int(allPoints[key][index])

        if value < currentMin:
            currentMin = value

    return currentMin


def getMaxCluster(cluster):
    max = Vector(0, 0)
    for i in range(len(cluster)):

        if cluster[i].getX() > max.getX():
            max.setX(cluster[i].getX())

        if cluster[i].getY() > max.getY():
            max.setY(cluster[i].getY())

    return max

def getMinCluster(cluster):
    min = Vector(float('inf'), float('inf'))
    for i in range(len(cluster)):

        if cluster[i].getX() < min.getX():
            min.setX(cluster[i].getX())

        if cluster[i].getY() < min.getY():
            min.setY(cluster[i].getY())

    return min


def setK(kVal: int):
    global k
    k = kVal

def printCentroids(centroids):
    for centroid in centroids:
        print("X: " + str(centroid.getX()) + ", Y: " + str(centroid.getY()))




def getVariation(clusterSet):
    variations = []
    for cluster in clusterSet:
        cMax_X = getMaxCluster(cluster).getX()
        cMin_Y = getMinCluster(cluster).getY()

        variations.append(abs(cMax_X - cMin_Y))
    
    totalVariation = sum(variations)
    return totalVariation



def k_mean(nrSimulations: int,index1: int, index2: int):
    
    # Runs the 2D k-mean algorithm on 2 datasets
    #
    #Args:
    #    nrSimulations: The number of times to simulate clusters.
    #    index1 : Data 1 from the data.txt file.
    #    index2 : Data 2 from the data.txt file.

    lowestVariation = float('inf')
    lowestVariationCluster = None
    finalCentroids = None
    for i in range(nrSimulations):
        finalClusters, finalCentroids = simulateCluster(index1, index2)
        clusterVariation = getVariation(finalClusters)
        if clusterVariation < lowestVariation:
            lowestVariation = clusterVariation
            lowestVariationCluster = finalClusters


    #Plotting

    print(lowestVariationCluster)
    for cluster in lowestVariationCluster:
        colorRGB = (random.random(), random.random(), random.random())
        for i in range(len(cluster)):
            plt.scatter(cluster[i].getX(), cluster[i].getY(), color=colorRGB)
            plt.pause(0.005)

    for centroid in finalCentroids:
        plt.scatter(centroid.getX(), centroid.getY(), marker="+", color=(0,0,0))
        plt.pause(0.005)
    plt.show()




def simulateCluster(index1, index2):
    maxIndex1, minIndex1 = getMaxPoints(allPoints ,index1), getMinPoints(allPoints, index1)
    maxIndex2, minIndex2 = getMaxPoints(allPoints ,index2), getMinPoints(allPoints, index2)
    centroids = [Vector(random.randrange(minIndex1, maxIndex1), random.randrange(minIndex2, maxIndex2)) for _ in range(k)]


        
    prevCentroids = []
    while True:

        clusters = updateClusters(allPoints, centroids, index1, index2)
        updateCentroids(centroids, clusters)

        if hasConverged(prevCentroids, centroids):
            print("Final centroids: ")
            printCentroids(centroids)
            return clusters, centroids
        else:
            prevCentroids = centroids

    


# Creates a new cluster 
def updateClusters(allPoints, centroids, index1, index2):
    newClusters = [
        [] for _ in centroids
    ]

    for key in allPoints:
        dataX = int(allPoints[key][index1])
        dataY = int(allPoints[key][index2])

        currentMin = float('inf')
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
    # Check if all current centroids have not moved significantly
    # compared to the previous centroids
    for c1, c2 in zip(currentCentroids, prevCentroids):
        if c1.getX() - c2.getX() != 0 or c1.getY() - c2.getY() != 0:
            return False

    return True


def getEuclideanDist(x1, y1, x2, y2) -> float:
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    
if __name__ == "__main__":
    formatData()
    setK(3)
    #Calculating k-mean for revenue and population
    k_mean(2 ,2, 4)


