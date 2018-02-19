# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def instruction_browsepages():
    # Cotegories instructions
    instructions = """
    Categories' commands:
    NBA       -- NBA
    MH        -- Monster Hunter World
    Gossiping -- Gossipings
    Sex       -- Sex
    Movie     -- Movies
    LoL       -- League of Legend
    Baseball  -- baseball
    (You can also enter other categories you know the name)

    exit      -- Leave program

    Please input Category and how many Pages to read:
                 (Default: LoL)        (Default: 1)
    """
    print(instructions)
    category = input("Category: ")
    page = input("Pages: ")
    return category, page


def browsepages(category, page):
        # Check whether there is a age 18 verification
        website18 = False
        older_page = None

        # Checking input(trun it to int)
        if not category:  # default of category
            category = 'LoL'
        if not page:  # default of page
            page = 1
        page = int(page)

        # Sending request to the website
        res = requests.get('https://www.ptt.cc/bbs/{}/index.html'.format(category))
        html_doc = res.text
        bs4_html = BeautifulSoup(html_doc, "html.parser")

        # If there is over18 website, answer "Yes"
        if bs4_html.find('div', {'class': 'over18-notice'}):
            payload = {
                'from': 'https://www.ptt.cc/bbs/{}/index.html'.format(category),
                'yes': 'yes'
            }
            rs = requests.session()
            res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
            res = rs.get('https://www.ptt.cc/bbs/{}/index.html'.format(category))
            html_doc = res.text
            bs4_html = BeautifulSoup(html_doc, "html.parser")
            website18 = True

        # Find pushes, titles, and urls in each page
        for i in range(1, page + 1):
            print("\n--------------------Page {}--------------------".format(i))
            print ("Pushes\t\tTitles\t\t\t\t\tUrls")
            articles = bs4_html.find_all("div", {"class": "r-ent"})
            for article in articles:
                push_number = article.find("div", {"class": "nrec"})
                title = article.find("div", {"class": "title"}).find('a')

                # Delete deleted articles and display pushes(display 0 if there is no push)
                if title:
                    if push_number.text:
                        print('[{}]\t{} \033[4mhttps://www.ptt.cc{}\033[0m'.format(push_number.text, title.text, title.get('href')))
                    else:
                        print('[{}]\t{} \033[4mhttps://www.ptt.cc{}\033[0m'.format('0', title.text, title.get('href')))

            # Get the url for the next page
            find_next_page = bs4_html.find_all('a', {"class": "btn wide"})
            for next_page in find_next_page:
                if next_page.text == "‹ 上頁":
                    older_page = 'https://www.ptt.cc{}'.format(next_page.get('href'))

            # If it is over18 website, use 18-age session for next website
            if website18:
                res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
                res = rs.get(older_page)
                html_doc = res.text
                bs4_html = BeautifulSoup(html_doc, "html.parser")

            # Sending request to the next website
            else:
                res = requests.get(older_page)
                html_doc = res.text
                bs4_html = BeautifulSoup(html_doc, "html.parser")


if __name__ == "__main__":
    while True:
        category, page = instruction_browsepages()
        browsepages(category, page)
