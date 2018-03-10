# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def find_hotboards():

    # Sending request to the website
    res = requests.get('https://www.ptt.cc/bbs/hotboards.html')
    html_doc = res.text
    bs4_html = BeautifulSoup(html_doc, "html.parser")
    hotboards = []

    boardnames = bs4_html.find_all("div", {"class": "board-name"})
    for boardname in boardnames:
        hotboards.append(boardname.text.lower())

    print(hotboards)


if __name__ == '__main__':
    find_hotboards()
