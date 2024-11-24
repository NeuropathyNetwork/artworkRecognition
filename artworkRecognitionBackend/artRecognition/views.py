from django.shortcuts import render


# from static.utils.crawler import fetch_baike_info
# Create your views here.


def index(request):
    return render(request, "index.html")


def analyze(request):
    # if request.method == 'POST':
    #     key_word = request.POST.get('key_word')
    #     result = fetch_baike_info(key_word)
    #     return render(request, 'analyze.html', {'result': result})
    # result = fetch_baike_info('莫奈')
    # print(result)
    # return render(request, 'analyze.html', {'result': result})
    return render(request, 'analyze.html')
