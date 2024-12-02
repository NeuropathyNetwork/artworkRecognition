from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .model_utils import load_model
import torch
from PIL import Image
from torchvision import transforms
import io
from .model_utils import Net
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from static.utils.crawler import fetch_baike_info
# Create your views here.

import numpy as np


def index(request):
    return render(request, "index.html")


# def analyze(request):
#     if request.method == 'POST':
#         key_word = request.POST.get('key_word')
#         result = fetch_baike_info(key_word)
#         result['author'] = key_word
#         return render(request, 'analyze.html', {'result': result})
#     result = fetch_baike_info('莫奈')
#     print(result)
#     return render(request, 'analyze.html', {'result': result})
# return render(request, 'analyze.html')

# 图片预处理（与训练时一致）
def preprocess_image(image_file):
    preprocess = transforms.Compose([
        transforms.Resize((300, 300)),  # 替换为您的模型输入尺寸
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 标准化参数
    ])
    image = Image.open(image_file).convert('RGB')
    image = preprocess(image)
    return image.unsqueeze(0)  # 增加 batch 维度


# 分析函数
def analyze(request):
    artists = {
        0: "弗里达·卡罗",
        1: "埃德加·德加",
        2: "彼得·勃鲁盖尔",
        3: "文森特·梵高",
        4: "伦勃朗",
        5: "亨利·卢梭",
        6: "亨利·马蒂斯",
        7: "胡安·米罗",
        8: "提香",
        9: "保罗·高更",
        10: "皮埃尔-奥古斯特·雷诺阿",
        11: "马克·夏加尔",
        12: "拉斐尔",
        13: "列奥纳多·达·芬奇",
        14: "阿梅代奥·莫迪利亚尼",
        15: "桑德罗·波提切利",
        16: "巴勃罗·毕加索",
        17: "雷内·马格里特",
        18: "瓦西里·康定斯基",
        19: "萨尔瓦多·达利",
        20: "米开朗基罗",
        21: "米哈伊尔·弗鲁贝尔",
        22: "保罗·克利",
        23: "卡米耶·毕沙罗",
        24: "乔托·迪·邦多纳",
        25: "居斯塔夫·库尔贝",
        26: "古斯塔夫·克里姆特",
        27: "亨利·德·图卢兹-洛特雷克",
        28: "弗朗西斯科·戈雅",
        29: "扬·范·艾克",
        30: "安德烈·鲁布廖夫",
        31: "安迪·沃霍尔",
        32: "阿尔弗雷德·西斯莱",
        33: "保罗·塞尚",
        34: "迭戈·委拉斯开兹",
        35: "爱德华·马奈",
        36: "彼得·保罗·鲁本斯",
        37: "克劳德·莫奈",
        38: "卡济米尔·马列维奇",
        39: "希罗尼穆斯·博斯",
        40: "卡拉瓦乔",
        41: "皮特·蒙德里安",
        42: "迭戈·里维拉",
        43: "埃尔·格列柯",
        44: "威廉·特纳",
        45: "乔治·修拉",
        46: "杰克逊·波洛克",
        47: "爱德华·蒙克",
        48: "欧仁·德拉克罗瓦"
    }
    if request.method == 'POST':
        # 从 POST 请求中提取图片
        image_file = request.FILES.get('image')
        if not image_file:
            return render(request, 'analyze.html', {'error': 'No image uploaded'})
        # Save the uploaded image

        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = os.path.join('/static/upload/', filename)
        try:

            # 加载模型
            model = load_model()
            model.eval()

            # 预处理图片
            input_image = preprocess_image(image_file)
            input_image = input_image.to('cuda' if torch.cuda.is_available() else 'cpu')

            with torch.no_grad():
                output = model(input_image)
                prediction = output.cpu().numpy()
                result = np.argmax(prediction, axis=1)[0]

            print(f"Prediction result: {result}, Prediction scores: {prediction[0].tolist()}")
            artist = artists[result]
            result = fetch_baike_info(artist)
            result['author'] = artist
            print(result)
            print(image_file)
            return render(request, 'analyze.html', {'result': result, 'image_url': image_url})


        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return render(request, 'analyze.html', {'error': str(e)})

    # 默认返回
    return render(request, 'analyze.html')
