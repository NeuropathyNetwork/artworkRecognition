import requests
from bs4 import BeautifulSoup
import urllib
import os

def fetch_baike_info(key_word):
    """
    从百度百科获取人物信息
    :param key_word: 百科关键字
    :return:一个包含人物简介、出生信息、逝世信息、代表作品的字典
    """
    url1 = 'https://baike.baidu.com/item/'
    key_word_encoded = urllib.parse.quote(key_word, encoding='utf-8', errors='replace')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    result = {
        "description": None,
        "birth_date": None,
        "death_date": None,
        "works": []
    }

    try:
        response = requests.get(url1 + key_word_encoded, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        # log_dir = 'logs'
        # if not os.path.exists(log_dir):
        #     os.makedirs(log_dir)
        # log_file_path = os.path.join(log_dir, f"{key_word_encoded}.html")
        # with open(log_file_path, 'w', encoding='utf-8') as log_file:
        #     log_file.write(response.text)
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            result["description"] = meta_description.get('content')

        dt_tag = soup.find('dt', class_='basicInfoItem_vbiBk itemName_fOdwv', string='出生日期')
        if dt_tag:
            dd_tag = dt_tag.find_next_sibling('dd', class_='basicInfoItem_vbiBk itemValue_JaQOj')
            if dd_tag:
                span_tag = dd_tag.find('span', class_='text_B_eob')
                if span_tag:
                    result["birth_date"] = span_tag.get_text(strip=True)

        dt_tag = soup.find('dt', class_='basicInfoItem_vbiBk itemName_fOdwv', string='逝世日期')
        if dt_tag:
            dd_tag = dt_tag.find_next_sibling('dd', class_='basicInfoItem_vbiBk itemValue_JaQOj')
            if dd_tag:
                span_tag = dd_tag.find('span', class_='text_B_eob')
                if span_tag:
                    result["death_date"] = span_tag.get_text(strip=True)

        # 获取代表作品
        dt_tag = soup.find('dt', class_='basicInfoItem_vbiBk itemName_fOdwv', string='代表作品')
        if dt_tag:
            dd_tag = dt_tag.find_next_sibling('dd', class_='basicInfoItem_vbiBk itemValue_JaQOj')
            if dd_tag:
                span_tags = dd_tag.find_all('span', class_='text_B_eob')
                for span in span_tags:
                    if span.get_text(strip=True) != "，":
                        result["works"].append(span.get_text(strip=True))

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"连接错误: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"超时错误: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"请求错误: {req_err}")
    except Exception as e:
        print(f"其他错误: {e}")

    return result

# if __name__ == '__main__':
#     artist = '梵高'
#     result = fetch_baike_info(artist)
#     print(result)
