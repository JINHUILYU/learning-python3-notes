import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os
import json

'''
    手写数字预测+特征提取

'''


# 预测类
class Pred:
    def __init__(self):
        self.labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        model_path = 'checkpoints/best_model.pth'
        # 加载模型
        self.model = torch.load(model_path)
        self.device = torch.device('gpu' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)

    # 预测
    def predict(self, img_path):
        transform = transforms.Compose([
            transforms.ToTensor()
        ])
        img = Image.open(img_path)
        img = img.convert('RGB')
        img = transform(img)
        img.resize_(1, 3, 28, 28)
        img = img.view(1, 3, 28, 28).to(self.device)
        output = self.model(img)
        output = torch.softmax(output, dim=1)
        # 每个预测值的概率
        probability = output.cpu().detach().numpy()[0]
        # 找出最大概率值的索引
        output = torch.argmax(output, dim=1)
        index = output.cpu().numpy()[0]
        # 预测结果
        pred = self.labels[index]
        print(pred, probability[index])
        return pred

def trans_square(image):
    r"""Open the image using PIL."""
    image = image.convert('RGB')
    w, h = image.size
    background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(255, 255, 255))  # 创建背景图，颜色值为127
    length = int(abs(w - h) // 2)  # 一侧需要填充的长度
    box = (length, 0) if w < h else (0, length)  # 粘贴的位置
    background.paste(image, box)
    return background


if __name__ == '__main__':
    # img_path = 'mnist/test/1/12.jpg'
    img_path = 'tmp.jpg'
    pred = Pred()
    res = pred.predict(img_path)
    # image = Image.open(img_path)
    # image.show()
    # image = trans_square(image)
    # image.show()
    # image = image.resize((28, 28))
    # image.save('tmp.jpg')
    # img_path = 'tmp.jpg'
    # image.show()
    print(res)
