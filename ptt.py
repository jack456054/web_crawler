# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


# Print cotegories instructions
def instruction_browsepages():
    instructions = """
    Instructions commands:
    Find      -- Find the popular articles in the specific category
    Browse    -- Browse the specific category


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

    Please input Instruction, Category and how many Pages to read:
    """
    print(instructions)


# Print error message
def error_msg():
    print("""
            ************************************
            *** Oops, something goes wrong!! ***
            ***                              ***
            ***      Please try again!!      ***
            ************************************
    """)
    help_msg()


def help_msg():
    # Help message
    print("""
    ### help      -- Look for instructions
    """)


# Catch user's input
def input_value():
    instruction = input("Instruction(Default: Browse): ")
    while instruction.lower() == 'help':
        instruction_browsepages()
        instruction = input("Instruction(Default: Browse): ")

    # User want to exit
    if instruction.lower() == 'exit':
        return 0, 0, 0
    category = input("Category(Default: LoL): ")
    while category.lower() == 'help':
        instruction_browsepages()
        category = input("Category(Default: LoL): ")

    # User want to exit
    if category.lower() == 'exit':
        return 0, 0, 0
    page = input("Pages(Default: 1): ")
    while category.lower() == 'help':
        instruction_browsepages()
        page = input("Pages(Default: 1): ")

    # User want to exit
    if page.lower() == 'exit':
        return 0, 0, 0
    return instruction, category, page


def check_valid_push(push):
    if push == '爆' or not push:
        return '99'
    elif int(push) == ValueError:  # NEED TO FIX THIS PART
        return '-1'
    elif int(push) > 99 or int(push) < 0:
        return '-1'
    else:
        return push


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

    # If cannot find the websit, print error message
    if not bs4_html.find('title'):
        error_msg()
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

        # If not next page, print error message
        if not older_page:
            error_msg()
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
    help_msg()


def find_articles(category, page, push):

    # Check whether there is a age 18 verification
    website18 = False
    older_page = None
    count_pages = 0

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
        error_msg()
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
    print ("Pushes\t\tTitles\t\t\t\t\tUrls")

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
                        print('[{}]\t{} \033[4mhttps://www.ptt.cc{}\033[0m'.format(push_number.text, title.text, title.get('href')))
                        count_pages += 1
                    else:
                        print('[{}]\t{} \033[4mhttps://www.ptt.cc{}\033[0m'.format('0', title.text, title.get('href')))
                        count_pages += 1
                elif push_number.text:
                    if (push_number.text)[0] == 'X':
                        continue
                    elif (push_number.text) == '爆' or int(push_number.text) >= int(push):
                        print('[{}]\t{} \033[4mhttps://www.ptt.cc{}\033[0m'.format(push_number.text, title.text, title.get('href')))
                        count_pages += 1

        # Get the url for the next page
        find_next_page = bs4_html.find_all('a', {"class": "btn wide"})
        for next_page in find_next_page:
            if next_page.text == "‹ 上頁":
                older_page = 'https://www.ptt.cc{}'.format(next_page.get('href'))

        # If not next page, print error message
        if not older_page:
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
    print("""
    ***   There are total {} articles   ***
    """.format(count_pages))
    help_msg()


if __name__ == "__main__":

    # Print instructions
    instruction_browsepages()

    # Repeated run until user what to exit
    while True:

        # Catch user's input
        instruction, category, page = input_value()

        # Check whether user what to exit
        if category == 0 and page == 0:
            print("""
                    ************************************
                    ***            Bye!!             ***
                    ************************************
            """)
            break

        elif instruction.lower() == 'find':
            push = input("Find the articles over how many pushes(From 0 to 99)(Default: 爆): ")
            push = check_valid_push(push)
            while push == '-1':
                push = input("Find the articles over how many pushes(From 0 to 99)(Default: 爆): ")
                push = check_valid_push(push)
            find_articles(category, page, push)

        # Go browse the website
        elif instruction.lower() == 'browse' or not instruction:
            browsepages(category, page)

        else:
            error_msg()
