# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import template
from bs4 import BeautifulSoup


# Catch user's input
def input_value():
    input_msg = 'Instruction(Default: Browse): '
    instruction = input(input_msg)

    # User want to exit or help
    whether_exit_help(instruction, input_msg)
    input_msg = 'Category(Default: LoL): '
    category = input(input_msg)

    # User want to exit or help
    whether_exit_help(category, input_msg)
    input_msg = 'Pages(Default: 1): '
    page = input(input_msg)

    # User want to exit
    whether_exit_help(page, input_msg)
    return instruction, category, page


# Check whether user what to exit
def whether_exit_help(user_input, input_msg):
    while user_input.lower() == 'help':
        template.instruction_browsepages()
        user_input = input(input_msg)
    if user_input.lower() == 'exit':
        template.bye_msg()
        exit()
    return user_input


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


# Sending request to the website and if there is over18 website, answer "Yes"
def over18(current_page):

    # Sending request to the website
    res = requests.get(current_page)
    html_doc = res.text
    bs4_html = BeautifulSoup(html_doc, "html.parser")

    # If there is over18 website, answer "Yes"
    if bs4_html.find('div', {'class': 'over18-notice'}):
        payload = {
            'from': current_page,
            'yes': 'yes'
        }
        rs = requests.session()
        res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
        res = rs.get(current_page)
        html_doc = res.text
        bs4_html = BeautifulSoup(html_doc, "html.parser")
    return bs4_html


def print_info(articles_info):
    print("{:7} {:50} {}".format('Pushes', 'URLs', 'Titles'))
    for index, (pushes, titles, urls) in enumerate(articles_info):
        print('[{}]\t\033[4mhttps://www.ptt.cc{:<30}\033[0m {:<50} '.format(pushes, urls, titles))


def browsepages(category, page):

    # Check whether there is a age 18 verification
    older_page = None
    articles_info = []

    # Checking input(trun it to int)
    if not category:  # default of category
        category = 'LoL'
    if not page:  # default of page
        page = 1
    page = int(page)
    current_page = ('https://www.ptt.cc/bbs/{}/index.html'.format(category))

    # Find pushes, titles, and urls in each page
    for i in range(1, page + 1):

        # Sending request and check over18 page
        bs4_html = over18(current_page)

        # If cannot find the websit, print error message
        if not bs4_html.find('title'):
            template.error_msg()
            return 0

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

        # Next page
        current_page = older_page
    template.help_msg()


def find_articles(category, page, push):

    # Check whether there is a age 18 verification
    older_page = None
    count_pages = 0
    articles_info = []

    # Checking input(trun it to int)
    if not category:  # default of category
        category = 'LoL'
    if not page:  # default of page
        page = 1
    page = int(page)

    current_page = ('https://www.ptt.cc/bbs/{}/index.html'.format(category))

    # Find pushes, titles, and urls in each page
    for i in range(1, page + 1):

        # Sending request and check over18 page
        bs4_html = over18(current_page)

        # If cannot find the websit, print error message
        if not bs4_html.find('title'):
            template.error_msg()
            return 0

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
            print_info(articles_info)
            print("""
            ***   There are total {} articles   ***
            """.format(count_pages))
            return 0

        # Next page
        current_page = older_page
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
        if instruction.lower() == 'find':
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
