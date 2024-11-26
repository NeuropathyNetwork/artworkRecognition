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


def analyze(request):
    if request.method == 'POST':
        key_word = request.POST.get('key_word')
        result = fetch_baike_info(key_word)
        result['author'] = key_word
        return render(request, 'analyze.html', {'result': result})
    result = fetch_baike_info('莫奈')
    print(result)
    return render(request, 'analyze.html', {'result': result})
    # return render(request, 'analyze.html')


# model = Net()
# model = load_model('static/resnet1722.pth', model)
# model.to(device)
#
#
# @csrf_exempt
# def predict(request):
#     if request.method == 'POST':
#         image_file = request.FILES['image']
#         image = Image.open(image_file).convert('RGB')
#
#         preprocess = transforms.Compose([
#             transforms.Resize(660),
#             transforms.CenterCrop(600),
#             transforms.ToTensor(),
#             transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#         ])
#         input_tensor = preprocess(image)
#         input_batch = input_tensor.unsqueeze(0)
#
#         device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         input_batch = input_batch.to(device)
#
#         with torch.no_grad():
#             output = model(input_batch)
#             _, predicted = torch.max(output, 1)
#             predicted_class = predicted.item()
#
#         return JsonResponse({'predicted_class': predicted_class})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
