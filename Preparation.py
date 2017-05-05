from VerificationCodeRecognition import ImageUtil
import os
from PIL import Image

def build_svm_file(filePath):
    root_path = './trainingSetImage/'
    fileList = os.listdir(root_path)
    for index,doc in enumerate(fileList):
        with open(filePath,'a') as f:
            for fileNum,imageFile in enumerate(os.listdir(root_path + doc)):
                image = Image.open(root_path + doc + '/' + imageFile)
                pixelList = ImageUtil.getFeature(image)
                featureString = str(index)
                for i,pixelNum in enumerate(pixelList):
                    tempStr = str(i + 1) + ':' + str(pixelNum)
                    featureString += ' ' + tempStr
                f.write(featureString + '\n')
                f.flush()
                print('已写入%d条记录' %(index * 100 + fileNum + 1))

def single_image_to_svm_file(image,char,filePath = './finaltest.txt'):
    with open(filePath, 'a') as f:
        pixelList = ImageUtil.getFeature(image)
        featureString = str(ord(char) - 65)
        for i, pixelNum in enumerate(pixelList):
            tempStr = ' ' + str(i + 1) + ':' + str(pixelNum)
            featureString += tempStr
        f.write(featureString + '\n')
        f.flush()