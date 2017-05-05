import os
import os.path
from numpy import *
from PIL import Image,ImageEnhance
from VerificationCodeRecognition import ImageCreator
from VerificationCodeRecognition import ImageUtil
from VerificationCodeRecognition import kNN

def imageDealer(image):
    threshold = 160
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 二值化
    image2 = image.convert('L')
    image2 = ImageEnhance.Sharpness(image2).enhance(3)
    image2 = image2.point(table, '1')
    # 去噪加剪枝10次
    for x in range(10):
        image2 = ImageUtil.clearNoise(image2, 100)
        image2 = ImageUtil.cutBranch(image2)
    cropImageList = ImageUtil.cropImageWithoutSave(image2)
    return cropImageList

def testkNNModel(testTimes):
    rightKeySet = []
    ImageList = []
    settingLabel = kNN.getLabelVector('./label.txt')
    dataSet = kNN.getDataSet('./model.txt')
    predictList = []
    rightCount = 0
    for n in range(testTimes):
        rightKey, vim = ImageCreator.draw_verify()
        rightKeySet.append(rightKey)
        ImageList.append(vim)
    for image in ImageList:
        cropImageList = imageDealer(image)
        string = ''
        for cropImage in cropImageList:
            testVector = ImageUtil.getTestData(cropImage)
            predict = kNN.kNNClassify(testVector,array(dataSet),settingLabel,3)
            string += predict
        predictList.append(string)
    for i in range(testTimes):
        print(predictList[i])
        if rightKeySet[i] == predictList[i]:
            print('预测正确' + predictList[i])
            rightCount += 1
    print('测试结束')
    print('正确率为%f' %(rightCount // testTimes))

if __name__ == '__main__':
    testkNNModel(3)