# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

#Cotegories instructions
print("Categories' commands:")
print("NBA\t\t-- NBA")
print("MH\t\t-- Monster Hunter World")
print("Gossiping\t-- Gossipings")#age 18 verification
print("Sex\t\t-- Sex")#age 18 verification
print("Movie\t\t-- Movies")
print("LoL\t\t-- League of Legend")
print("Baseball\t-- baseball")
print("\033[4mexit\033[0m\t\t-- \033[4mLeave program\033[0m")
print("(You can also enter other categories you know the name)")

#Repeat program until exit
while True:

    #Check whether there is a age 18 verification
    website18 = False

    #Checking input(trun it to int)
    category = input("\nPlease input \033[4mcategory's\033[0m name(default: LoL):")
    if category == 'exit':
        break
    if not category:#default of category
        category = 'LoL'
    page = input("Please input how many \033[4mpages\033[0m you want to read(from newest to oldest)(default: 1):")
    if not page:#default of page
        page = 1
    if page == 'exit':
        break
    page = int(page)

    #Sending request to the website
    res = requests.get('https://www.ptt.cc/bbs/{}/index.html'.format(category))
    html_doc = res.text
    bs4_html = BeautifulSoup(html_doc, "html.parser")

    #If there is over18 website, answer "Yes"
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

    #Find pushes, titles, and urls in each page
    for i in range(1,page+1):
        print("\n--------------------Page {}--------------------".format(i))
        print ("Pushes\t\tTitles\t\t\t\t\tUrls")
        articles = bs4_html.find_all("div", {"class": "r-ent"})
        for article in articles:
            push_number = article.find("div", {"class": "nrec"})
            title = article.find("div", {"class": "title"}).find('a')

            #Delete deleted articles and display pushes(display 0 if there is no push)
            if title:
                if push_number.text:
                    print('[{}]\t{} \033[4mhttps://www.ptt.cc{}\033[0m'.format(push_number.text,title.text, title.get('href')))
                else:
                    print('[{}]\t{} \033[4mhttps://www.ptt.cc{}\033[0m'.format('0',title.text, title.get('href')))

        #Get the url for the next page
        find_next_page = bs4_html.find_all('a', {"class": "btn wide"})
        for next_page in find_next_page:
            if next_page.text == "‹ 上頁":
                older_page = 'https://www.ptt.cc{}'.format(next_page.get('href'))

        #If it is over18 website, use 18-age session for next website
        if website18:
            res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
            res = rs.get(older_page)
            html_doc = res.text
            bs4_html = BeautifulSoup(html_doc, "html.parser")

        #Sending request to the next website
        else:
            res = requests.get(older_page)
            html_doc = res.text
            bs4_html = BeautifulSoup(html_doc, "html.parser")
