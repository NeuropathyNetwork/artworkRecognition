from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .model_utils import load_model
import torch
from PIL import Image
from torchvision import transforms
import io
from .model_utils import Net


from static.utils.crawler import fetch_baike_info
# Create your views here.


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
    if request.method == 'POST':
        # 从 POST 请求中提取图片
        image_file = request.FILES.get('image')
        if not image_file:
            return render(request, 'analyze.html', {'error': 'No image uploaded'})

        try:
            # 加载模型
            model = load_model()
            model.eval()

            # 预处理图片
            input_image = preprocess_image(image_file)
            input_image = input_image.to('cuda' if torch.cuda.is_available() else 'cpu')

            # 推理
            with torch.no_grad():
                output = model(input_image)
                prediction = output.cpu().numpy()
                result = np.argmax(prediction, axis=1)[0]  # 获取分类结果索引

            # 根据分类索引，生成解释或分析

            return render(request, 'analyze.html', {'result': {'label': result, 'score': prediction[0].tolist()}})

        except Exception as e:
            return render(request, 'analyze.html', {'error': str(e)})

    # 默认返回
    return render(request, 'analyze.html')
