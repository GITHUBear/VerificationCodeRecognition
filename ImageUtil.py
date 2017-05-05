from PIL import Image
import os.path
import os

def floodFill(image,x,y,bookList,vol):
    '''经典的floodfill算法
    :parameter  image(图片对象) x(像素位置x坐标) y(像素位置y坐标) bookList(记录是否访问过) vol(判定体积)
    :return dotList(体积小于vol的连通图的点集)
    '''
    L, dotList = [(x,y)], [(x,y)]
    while len(L) != 0:
        spanLeft = False
        spanRight = False
        x,y = L.pop(0)
        bookList[y][x] = 1
        while y >= 0 and image.getpixel((x, y)) == 0:
            y -= 1
            if y >= 0 and image.getpixel((x, y)) == 0:
                bookList[y][x] = 1
                dotList.append((x, y))
        y += 1
        while y < image.size[1] and image.getpixel((x, y)) == 0:
            if not bookList[y][x]:
                bookList[y][x] = 1
                dotList.append((x,y))
            if (not spanLeft) and x > 0 and image.getpixel((x - 1,y)) == 0 and (not bookList[y][x - 1]):
                bookList[y][x - 1] = 1
                L.append((x - 1, y))
                dotList.append((x - 1, y))
                spanLeft = True
            elif spanLeft and x > 0 and image.getpixel((x - 1,y)) == 1:
                spanLeft = False
            if (not spanRight) and x < image.size[0] - 1 and image.getpixel((x + 1,y)) == 0 and (not bookList[y][x + 1]):
                bookList[y][x + 1] = 1
                L.append((x + 1, y))
                dotList.append((x + 1, y))
                spanRight = True
            elif spanRight and x < image.size[0] - 1 and image.getpixel((x + 1,y)) == 1:
                spanRight = False
            y += 1
    if len(L) == 0 and len(dotList) < vol + 1:
        return dotList
    else:
        return None

def clearNoise(image, vol):
    '''
    去噪函数
    :param image: 图片对象
    :param vol: 判定体积
    :return: 去噪后的图片对象
    '''
    bookList = [[0]*image.size[0] for _ in range(image.size[1])]
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if image.getpixel((x, y)) == 1 or bookList[y][x]:
                continue
            else:
                #print('%d %d pixel is going to floodfill,the color is %d' %(x,y,image.getpixel((x,y))))
                dotList = floodFill(image, x, y, bookList,vol)
                #print(dotList)
                if dotList:
                    for dot in dotList:
                        image.putpixel(dot,1)
    return image

def cutBranch(image):
    '''
    剪枝函数
    :param image: 图片对象
    :return: 剪枝后的图片对象
    '''
    image2 = image
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            dotNum = 0
            if image.getpixel((x,y)) == 1:
                continue
            else:
                if x > 0 and image.getpixel((x - 1, y)) == 0:
                    dotNum += 1
                if x < image.size[0] - 1 and image.getpixel((x + 1, y)) == 0:
                    dotNum += 1
                if y > 0 and image.getpixel((x, y - 1)) == 0:
                    dotNum += 1
                if y < image.size[1] - 1 and image.getpixel((x, y + 1)) == 0:
                    dotNum += 1
                if x > 0 and y > 0 and image.getpixel((x - 1, y - 1)) == 0:
                    dotNum += 1
                if x > 0 and y < image.size[1] - 1 and image.getpixel((x - 1, y + 1)) == 0:
                    dotNum += 1
                if x < image.size[0] - 1 and y > 0 and image.getpixel((x + 1, y - 1)) == 0:
                    dotNum += 1
                if x < image.size[0] - 1 and y < image.size[1] - 1 and image.getpixel((x + 1, y + 1)) == 0:
                    dotNum += 1
            if dotNum < 4:
                image2.putpixel((x, y),1)
    return image2

def cropImage(Image,char,filePath = './trainingSetImage/'):
    '''
    图像裁剪
    :param Image: 需要裁剪的图片对象
    :param filePath:
    :return:
    '''
    fileNum = len(os.listdir(filePath + char + '/'))
    for i in range(4):
        y = 10
        x = 60 * i + 10
        subImage = Image.crop((x,y,x + 40,y + 40))
        subImage.save(filePath + char + '/' + str(fileNum + i) + '.JPG')

def cropImageWithoutSave(Image):
    ImageList = []
    for i in range(4):
        y = 10
        x = 60 * i + 10
        subImage = Image.crop((x,y,x + 40,y + 40))
        ImageList.append(subImage)
    return ImageList

def getFeature(image):
    '''
    从图片中获取特征
    :param image:
    :return: 特征向量
    '''
    pixelNumberList = []
    for y in range(image.size[1]):
        num = 0
        for x in range(image.size[0]):
            if image.getpixel((x,y)) == 0:
                num += 1
        pixelNumberList.append(num)
    for x in range(image.size[0]):
        num2 = 0
        for y in range(image.size[1]):
            if image.getpixel((x,y)) == 0:
                num2 += 1
        pixelNumberList.append(num2)
    return pixelNumberList

def image2Vector(rootFilePath,imageSize,destFilePath):
    width = imageSize[0]
    height = imageSize[1]
    labels = []
    with open(destFilePath,'w') as destF:
        for index1,imagePackage in enumerate(os.listdir(rootFilePath)):
            imagePackagePath = rootFilePath + '/' + imagePackage
            for index2,images in enumerate(os.listdir(imagePackagePath)):
                labels.append(imagePackage[0])
                imagePath = imagePackagePath + '/' + images
                image = Image.open(imagePath)
                for x in range(width):
                    for y in range(height):
                        pixel = image.getpixel((x,y))
                        if pixel == 255:
                            destF.write('1')
                        else:
                            destF.write('0')
                destF.write('\n')
                print('已处理%d张图片' %(index1 * 100 + index2))
    return labels

def getTestData(image):
    testVector = []
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixel = image.getpixel((x, y))
            if pixel == 255:
                testVector.append(1)
            else:
                testVector.append(0)
    return testVector