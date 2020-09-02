from bs4 import BeautifulSoup
import urllib.request
import json
import re


def gen_katakana_json(urls):
    result = []
    for url in urls:
        katakana_soup = get_soup(url)
        katakana_json = katakanawords_to_json(katakana_soup)
        result.extend(katakana_json)
    return result


def gen_myoji_json(file):
    myoji_soup = BeautifulSoup(open(file), "lxml")
    myoji_json = myoji_to_json(myoji_soup)
    return myoji_json


def get_soup(url):
    print(url+" 取得中")
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    return soup


def katakanawords_to_json(soup):
    words = soup.find_all("p")[1]  # 2個目のpがワードリスト
    words_parsed = words.text.replace(
        "\u3000", "").split("\n")  # 改行で名前・キャプションをパース

    words_dictlist = []
    for (i, word) in enumerate(words_parsed):
        # 名前をカタカナと英語に整理
        if i % 2 == 0:
            kana_name = re.split("[（(]", word[1:])[0]
            en_name = re.split("[)）]", re.split("[（(]", word[1:])[1])[0]

        # 辞書型に格納しリストに追加
        elif i % 2 == 1:
            words_dict = {"second_name": kana_name,
                          "second_name_original": en_name,
                          "caption": word}
            words_dictlist.append(words_dict)

    return words_dictlist


def myoji_to_json(soup):
    rows = soup.find_all("tr")
    names_dictlist = []
    name_dict = {}
    for row in rows:
        try:
            rank = row.find_all("td")[0].text
            myoji = row.find_all("td")[1].text
            yomi = re.sub("[★☆]", "", row.find_all("td")[4].text)
        except:
            continue
        name_dict = {"name": myoji, "name_read": yomi, "rank": rank}
        names_dictlist.append(name_dict)

    return names_dictlist


if __name__ == "__main__":

    # カタカナ語スクレイピング
    katakana_urls = [
        "https://kakkoii-yougosyuu.com/archives/1035333396.html",
        "https://kakkoii-yougosyuu.com/archives/katakanakagyou.html",
        "https://kakkoii-yougosyuu.com/archives/1036149936.html",
        "https://kakkoii-yougosyuu.com/archives/katakanatagyou.html",
        "https://kakkoii-yougosyuu.com/archives/katakananagyou.html",
        "https://kakkoii-yougosyuu.com/archives/1036170595.html",
        "https://kakkoii-yougosyuu.com/archives/katakanamagyou.html",
        "https://kakkoii-yougosyuu.com/archives/katakanayarawa.html",
    ]
    katakana_words = gen_katakana_json(katakana_urls)

    # カタカナ語jsonをファイル出力
    with open("./json/katakana.json", 'w') as outfile:
        json.dump(katakana_words, outfile,  ensure_ascii=False)

    # 名字スクレイピング（htmlファイルから）
    myoji_file = "./myoji.html"
    myoji_words = gen_myoji_json(myoji_file)

    # 名字jsonをファイル出力
    with open("./json/myoji.json", 'w') as outfile:
        json.dump(myoji_words, outfile,  ensure_ascii=False)
