import numpy as np
import operator
from os import listdir

def kNNClassify(newVector,dataSet,label,k):
    dataSetSize = dataSet.shape[0]
    newMatrix = np.tile(newVector,(dataSetSize,1))
    sqrMatrix = (dataSet - newMatrix) ** 2
    sqrDistant = sqrMatrix.sum(axis=1)
    sortedDistantIndex = sqrDistant.argsort()
    classes = {}
    for i in range(k):
        choosedLabel = label[sortedDistantIndex[i]]
        classes[choosedLabel] = classes.get(choosedLabel,0) + 1
    sortedClasses = sorted(classes.items(),key = operator.itemgetter(1),reverse = True)
    return sortedClasses[0][0]

def getDataSet(dataSetFilePath):
    dataSet = []
    with open(dataSetFilePath,'r') as dataF:
        done = False
        while not done:
            fileStr = dataF.readline()
            if fileStr != '':
                dataSet.append([int(data) for data in fileStr if not data == '\n'])
            else:
                done = True
    return dataSet

def getLabelVector(labelFilePath):
    label = []
    with open(labelFilePath,'r') as labelF:
        fileStr = labelF.readline()
        for singleLabel in fileStr:
            label.append(singleLabel)
    return label

def createLabelFile(destFile,labels):
    with open(destFile,'w') as destF:
        for label in labels:
            destF.write(label)
        destF.write('\n')