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




class kommunDataSet():

    def __init__(self, dataFile: str):
        self.data = dataFile


    def hasNumbers(self, inputStr: str):
        return bool(re.search(r"\d", inputStr))

    def formatData(self, allPoints: dict):
        with open(self.data, "r") as f:
            f.readline() #Removes first unecessary line

            currentKey = 0
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    elements = line.split()

                    #Mergin cities that has names with space: [Upplands, Väsby] -> [Upplands Väsby,]
                    if not self.hasNumbers(elements[3]):
                        elements[2] = elements[2] + " " + elements[3]
                        del elements[3]

                    for i in range(len(elements)):
                        if currentKey in allPoints.keys():
                            allPoints[currentKey].append(elements[i])
                        else:
                            allPoints[currentKey] = []
                            allPoints[currentKey].append(elements[i])

                currentKey = currentKey + 1


    def printCitiesFromCluster(self, data: dict, clusters, index: int):
        printStr = ""
        currentCluster = 0
        for cluster in clusters:
            tempStr = ""
            tempStr = tempStr + "\n Cluster " + str(currentCluster) + ": \n"
            #Ex cluster: [[1,2,3], [4,5,6], [7,8,9]]
            for i in range(len(cluster)):
                for key in data:
                    for j in range(len(data[key])):
                        if self.hasNumbers(data[key][j]) and (float(data[key][j]) == cluster[i].getX() or float(data[key][j]) == cluster[i].getY()):
                            tempStr = tempStr + " " + data[key][index] + ", "
                            break
            
            printStr = printStr + tempStr
            currentCluster = currentCluster + 1

        print(printStr)


class K_2D_Means():

    def __init__(self, nrSimulations: int, allPoints: dict, k: int, index1: int, index2: int):
        self.nrSimulations = nrSimulations
        self.allPoints = allPoints
        self.k = k
        self.index1 = index1
        self.index2 = index2

        # The final cluster an centroids in list of vectors
        self.finalCluster = None
        self.finalCentroids = None
        self.k_mean(100)


        
        

    def k_mean(self, nrSimulations: int):
    
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
            finalClusters, finalCentroids = self.simulateCluster()
            clusterVariation = self.getVariation(finalClusters)
            if clusterVariation < lowestVariation:
                lowestVariation = clusterVariation
                lowestVariationCluster = finalClusters

        self.finalCluster = lowestVariationCluster
        self.finalCentroids = finalCentroids


    def plotClusters(self):
        for cluster in self.finalCluster:
            colorRGB = (random.random(), random.random(), random.random())
            for i in range(len(cluster)):
                plt.scatter(cluster[i].getX(), cluster[i].getY(), color=colorRGB)
                plt.pause(0.005)
        plt.show()

    def plotCentroids(self):
        for centroid in self.finalCentroids:
            plt.scatter(centroid.getX(), centroid.getY(), marker="+", color=(0,0,0))
            plt.pause(0.005)
        plt.show()


    def getFinalClusters(self):
        return self.finalCluster

    def getMaxPoints(self, allPoints: dict ,index: int) -> float:
        # Get a list of all the values at the given index in the allPoints dictionary
        values = [float(allPoints[key][index]) for key in allPoints]
        # Return the maximum value from the list
        return max(values)

    def getMinPoints(self, allPoints ,index: int) -> float:
        # Get a list of all the values at the given index in the allPoints dictionary
        values = [float(allPoints[key][index]) for key in allPoints]
        # Return the minimum value from the list
        return min(values)


    def getMaxCluster(self, cluster):
        max = Vector(0, 0)
        for i in range(len(cluster)):

            if cluster[i].getX() > max.getX():
                max.setX(cluster[i].getX())

            if cluster[i].getY() > max.getY():
                max.setY(cluster[i].getY())

        return max

    def getMinCluster(self, cluster):
        min = Vector(float('inf'), float('inf'))
        for i in range(len(cluster)):

            if cluster[i].getX() < min.getX():
                min.setX(cluster[i].getX())

            if cluster[i].getY() < min.getY():
                min.setY(cluster[i].getY())

        return min


    def printCentroids(self, centroids):
        for centroid in centroids:
            print("X: " + str(centroid.getX()) + ", Y: " + str(centroid.getY()))



    def getVariation(self, clusterSet):
        variations = []
        for cluster in clusterSet:
            cMax_X = self.getMaxCluster(cluster).getX()
            cMin_Y = self.getMinCluster(cluster).getY()

            variations.append(abs(cMax_X - cMin_Y))
    
        totalVariation = sum(variations)
        return totalVariation

    def getRandomCentroidPos(self):
        maxIndex1, minIndex1 = self.getMaxPoints(self.allPoints ,self.index1), self.getMinPoints(self.allPoints, self.index1)
        maxIndex2, minIndex2 = self.getMaxPoints(self.allPoints ,self.index2), self.getMinPoints(self.allPoints, self.index2)
        centroidPos = Vector(random.randrange(minIndex1, maxIndex1), random.randrange(minIndex2, maxIndex2))
        return centroidPos

    def simulateCluster(self):
        maxIndex1, minIndex1 = self.getMaxPoints(self.allPoints ,self.index1), self.getMinPoints(self.allPoints, self.index1)
        maxIndex2, minIndex2 = self.getMaxPoints(self.allPoints ,self.index2), self.getMinPoints(self.allPoints, self.index2)
        centroids = [self.getRandomCentroidPos() for _ in range(self.k)]


        
        prevCentroids = None
        while True:

            clusters = self.updateClusters(self.allPoints, centroids, self.index1, self.index2)
            self.updateCentroids(centroids, clusters)

            if prevCentroids != None and self.hasConverged(prevCentroids, centroids):
                print("Final centroids: ")
                self.printCentroids(centroids)
                return clusters, centroids
        
            prevCentroids = centroids

    


    # Creates a new cluster 
    def updateClusters(self, allPoints, centroids, index1, index2):
        newClusters = [
            [] for _ in centroids
        ]

        for key in allPoints:
            dataX = float(allPoints[key][index1])
            dataY = float(allPoints[key][index2])

            currentMin = float('inf')
            index = 0
            for i in range(len(centroids)):
                centroidX = centroids[i].getX()
                centroidY = centroids[i].getY()

                eucDist = self.getEuclideanDist(dataX, dataY, centroidX, centroidY)
                if eucDist < currentMin:
                    currentMin = eucDist
                    index = i


            # When finished comparing value insert with correct centroid
            newClusters[index].append(Vector(dataX, dataY))


        # Checking edge case for when a centroid has bad
        # starting position and is not assigned any points
        #for i in range(len(newClusters)):
            #if(len(newClusters[i]) == 0):
                #newClusters[i].append(Vector(0, 0))
                #ADD SOMETHING TO FIX THIS

        return newClusters



    def updateCentroids(self, centroids, newClusters):
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

            if len(newClusters[i]) == 0:
                newClusters[i].append(self.getRandomCentroidPos())
                break

            # Calculate the average x and y coordinates
            avgX = sumX/len(newClusters[i])
            avgY = sumY/len(newClusters[i])
            #Update the position of the centroid
            centroids[i].changePos(avgX, avgY)



    def hasConverged(self ,prevCentroids, currentCentroids) -> bool:
        # Check if all current centroids have not moved significantly
        # compared to the previous centroids
        for c1, c2 in zip(currentCentroids, prevCentroids):
            if c1.getX() - c2.getX() != 0 or c1.getY() - c2.getY() != 0:
                return False

        return True


    def getEuclideanDist(self, x1, y1, x2, y2) -> float:
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# allPoints dictionary
# keys: 0 - 207
# indexes:
#   0: Kommun_code
#   1: Year
#   2: Kommun_name
#   3: Revenue
#   4: Employee
#   5: Population
#   6: Population_University
#   7: Percent_University
#   8: Productivity
#   9: SalesIndex
#   10: Infrast
#   11: Border
    
if __name__ == "__main__":
    allPoints = {}
    data = kommunDataSet("data.txt")
    data.formatData(allPoints)
    #Calculating k-mean for revenue and population
    kMeans = K_2D_Means(nrSimulations=100, allPoints=allPoints, k=5, index1=0, index2=5)
    
    finalCluster = kMeans.getFinalClusters()
    data.printCitiesFromCluster(allPoints, finalCluster, 2)
    
    kMeans.plotClusters()
    


