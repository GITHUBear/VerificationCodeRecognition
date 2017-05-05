from PIL import Image,ImageEnhance
from pylab import *
from VerificationCodeRecognition import ImageCreator
from VerificationCodeRecognition import ImageUtil

#rightKey, vim = ImageCreator.draw_verify()
#vim.save('./Image/' + rightKey + '.JPG')

threshold = 160
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

for i in range(26):
    for j in range(25):
        char = chr(ord('A') + i)
        vim = ImageCreator.draw_identified_pic(char)
        vim.save('./Image/' + char + str(j) + '.JPG')
        print('成功生成第%d张图片' %(i * 26 + j))

num = 0
for imageFile in os.listdir('./Image'):
    image = Image.open('./Image/' + imageFile)
    char = imageFile[0]
    # 原图
    #subplot(131)
    #title('pure pic')
    #imshow(image)
    # 二值化
    image = image.convert('L')
    image = ImageEnhance.Sharpness(image).enhance(3)
    image = image.point(table, '1')
    #subplot(132)
    #title('binary')
    #imshow(image)
    #去噪加剪枝
    for x in range(10):
        image = ImageUtil.clearNoise(image,100)
        image = ImageUtil.cutBranch(image)
    #subplot(133)
    #title('do more times')
    #imshow(image)

    #show()

    ImageUtil.cropImage(image,char)
    num += 4
    print('成功将%d张图片放入训练集' %(num))

    os.remove('./Image/' + imageFile)

    #image.save('./trainingSetImage/' + imageFile)