from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


# 模拟模型的占位逻辑
def dummy_model(image_path):
    # 替换为你的模型调用逻辑
    # 这里只是返回一个固定结果
    return {
        "author": "Vincent van Gogh",
        "confidence": 0.92
    }


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # 获取上传的图片
        image_file = request.FILES['image']
        file_path = default_storage.save(f"uploads/{image_file.name}", ContentFile(image_file.read()))

        # 模型占位调用
        result = dummy_model(file_path)

        # 返回结果
        return JsonResponse({
            "success": True,
            "message": "Image processed successfully.",
            "result": result
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "Invalid request. Please upload an image."
        })
