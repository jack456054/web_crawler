# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import template
from bs4 import BeautifulSoup


# Catch user's input
def input_value():
    instruction = input("Instruction(Default: Browse): ")
    while instruction.lower() == 'help':
        template.instruction_browsepages()
        instruction = input("Instruction(Default: Browse): ")

    # User want to exit
    if instruction.lower() == 'exit':
        return 0, 0, 0
    category = input("Category(Default: LoL): ")
    while category.lower() == 'help':
        template.instruction_browsepages()
        category = input("Category(Default: LoL): ")

    # User want to exit
    if category.lower() == 'exit':
        return 0, 0, 0
    page = input("Pages(Default: 1): ")
    while page.lower() == 'help':
        template.instruction_browsepages()
        page = input("Pages(Default: 1): ")

    # User want to exit
    if page.lower() == 'exit':
        return 0, 0, 0
    return instruction, category, page


# Check whether is valid input
def check_valid_push(push):
    while True:
        try:
            if push == '爆' or not push:
                return '100'
            elif int(push) > 99 or int(push) < 0:
                return '-1'
            else:
                return push

        # Check whether type correct
        except ValueError:
            return '-1'


def print_info(articles_info):
    for index, (pushes, titles, urls) in enumerate(articles_info):
        print('[{}]\t\033[4mhttps://www.ptt.cc{:<30}\033[0m {:<50} '.format(pushes, urls, titles))


def browsepages(category, page):

    # Check whether there is a age 18 verification
    website18 = False
    older_page = None
    articles_info = []

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

    # If cannot find the websit, print error message
    if not bs4_html.find('title'):
        template.error_msg()
        return 0

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
        articles_info = []
        articles = bs4_html.find_all("div", {"class": "r-ent"})
        for article in articles:
            push_number = article.find("div", {"class": "nrec"})
            title = article.find("div", {"class": "title"}).find('a')

            # Delete deleted articles and display pushes(display 0 if there is no push)
            if title:
                if push_number.text:
                    articles_info.append([push_number.text, title.text, title.get('href')])
                else:
                    articles_info.append(['0', title.text, title.get('href')])
        print("\n--------------------Page {}--------------------".format(i))
        print("Pushes\t\tUrls\t\t\t\t\t\tTitles")
        print_info(articles_info)
        # Get the url for the next page
        find_next_page = bs4_html.find_all('a', {"class": "btn wide"})
        for next_page in find_next_page:
            if next_page.text == "‹ 上頁":
                older_page = 'https://www.ptt.cc{}'.format(next_page.get('href'))

        # If not next page, print error message
        if not older_page:
            template.error_msg()
            return 0

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
    template.help_msg()


def find_articles(category, page, push):

    # Check whether there is a age 18 verification
    website18 = False
    older_page = None
    count_pages = 0
    articles_info = []

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

    # If cannot find the websit, print error message
    if not bs4_html.find('title'):
        template.error_msg()
        return 0

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
        articles = bs4_html.find_all("div", {"class": "r-ent"})
        for article in articles:
            push_number = article.find("div", {"class": "nrec"})
            title = article.find("div", {"class": "title"}).find('a')

            # Delete deleted articles and display pushes(display 0 if there is no push)
            if title:
                if push == '0':
                    if push_number.text:
                        articles_info.append([push_number.text, title.text, title.get('href')])
                        count_pages += 1
                    else:
                        articles_info.append(['0', title.text, title.get('href')])
                        count_pages += 1
                elif push_number.text:
                    if (push_number.text)[0] == 'X':
                        continue
                    elif (push_number.text) == '爆' or int(push_number.text) >= int(push):
                        articles_info.append([push_number.text, title.text, title.get('href')])
                        count_pages += 1

        # Get the url for the next page
        find_next_page = bs4_html.find_all('a', {"class": "btn wide"})
        for next_page in find_next_page:
            if next_page.text == "‹ 上頁":
                older_page = 'https://www.ptt.cc{}'.format(next_page.get('href'))

        # If not next page, print error message
        if not older_page:
            print("Pushes\t\tUrls\t\t\t\t\t\tTitles")
            print_info(articles_info)
            print("""
            ***   There are total {} articles   ***
            """.format(count_pages))
            return 0

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
    print("Pushes\t\tUrls\t\t\t\t\t\tTitles")
    print_info(articles_info)
    print("""
    ***   There are total {} articles   ***
    """.format(count_pages))
    template.help_msg()


if __name__ == "__main__":

    # Print instructions
    template.instruction_browsepages()

    # Repeated run until user what to exit
    while True:

        # Catch user's input
        instruction, category, page = input_value()

        # Check whether user what to exit
        if category == 0 and page == 0:
            template.bye_msg()
            break

        elif instruction.lower() == 'find':
            push = input("Find the articles over how many pushes(From 0 to 99)(Default: 爆): ")
            push = check_valid_push(push)

            # Check whether is valid input
            while push == '-1':
                print("""
                        *** Please insert 0 to 99 or '爆' ***
                """)
                push = input("Find the articles over how many pushes(From 0 to 99)(Default: 爆): ")
                push = check_valid_push(push)
            find_articles(category, page, push)

        # Go browse the website
        elif instruction.lower() == 'browse' or not instruction:
            browsepages(category, page)

        else:
            template.error_msg()
