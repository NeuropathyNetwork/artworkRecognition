import requests
from bs4 import BeautifulSoup
import urllib


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
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            result["description"] = meta_description.get('content')

        dt_tag = soup.find('dt', class_='basicInfoItem_X788I itemName_H4xlK', string='出生日期')
        if dt_tag:
            dd_tag = dt_tag.find_next_sibling('dd', class_='basicInfoItem_X788I itemValue_I6jX1')
            if dd_tag:
                span_tag = dd_tag.find('span', class_='text_X0TgX')
                if span_tag:
                    result["birth_date"] = span_tag.get_text(strip=True)

        dt_tag = soup.find('dt', class_='basicInfoItem_X788I itemName_H4xlK', string='逝世日期')
        if dt_tag:
            dd_tag = dt_tag.find_next_sibling('dd', class_='basicInfoItem_X788I itemValue_I6jX1')
            if dd_tag:
                span_tag = dd_tag.find('span', class_='text_X0TgX')
                if span_tag:
                    result["death_date"] = span_tag.get_text(strip=True)

        # 获取代表作品
        dt_tag = soup.find('dt', class_='basicInfoItem_X788I itemName_H4xlK', string='代表作品')
        if dt_tag:
            dd_tag = dt_tag.find_next_sibling('dd', class_='basicInfoItem_X788I itemValue_I6jX1')
            if dd_tag:
                span_tags = dd_tag.find_all('span', class_='text_X0TgX')
                for span in span_tags:
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
