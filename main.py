import re

allData = {}


def createKeys():
    with open("data.txt", "r") as f:
        f.readline()
        while True:
            line = f.readline()
            
            if not line:
                break
            else:
                prevChar = ""
                kommunCode = ""
                for char in line:
                    if char != " ":
                        kommunCode = kommunCode + char
                    elif prevChar != " " and char == " ":
                        allData[kommunCode] = []
                        break 

                    prevChar = char
            

def cleanData():
    with open("data.txt", "r") as f:
        f.readline() #Removes first unecessary line
        
        while True:
            line = f.readline()
            passedKommunCode = False
            kommunCode = ""

            if not line:
                break
            else:
                prevChar = ""
                data = ""
                for char in line:
                    # Adds the char to data if not empty
                    if char != " ":
                        data = data + char
                        
                    # At the end of data inputs into dict
                    elif prevChar != " " and char == " " and passedKommunCode == False:
                        passedKommunCode = True
                        kommunCode = data
                        data = ""
                    elif prevChar != " " and char == " " and passedKommunCode == True:
                        if kommunCode in allData:
                            allData[kommunCode].append(data)
                        else:
                            allData[kommunCode] = []
                            allData[kommunCode].append(data)
                        data = ""
                        
                    prevChar = char

            
            


if __name__ == "__main__":
    cleanData()
    print(allData)