import requests
from bs4 import BeautifulSoup
import pandas as pd
from constants import URL, PROFILE_URL, CSV_NAME

def get_last_page():
    first = requests.get(URL)
    soup = BeautifulSoup(first.text, 'html.parser')
    final_page = soup.select('#main-content > div > section > nav > ul > li:nth-child(12) > a')[0]['href']
    fp = final_page.split('=')[-1]
    return int(fp)

def check_department(researcher):
    l1 = researcher.find('div', class_='rendering_person_short')
    for span in l1.find_all('span'):
        # Check department
        if span.text == str('Centre for Intelligent Healthcare'):
            name = researcher.find('h3', class_='title').find('span').text
            return name
        else:
            pass

def create_csv():
    database = pd.DataFrame(columns=['Title', 'Author', 'Published', 'Link'])
    database.to_csv(CSV_NAME)

# def update_csv(database):
#     current_data = pd.read_csv(database, index_col="Unnamed: 0")
#     return current_data

def add_each_researchers_publication(researcher, url):
    new_url = url + str(researcher).replace(' ','-').lower() + '/publications/'
    page = requests.get(new_url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="main-content")
    if results is None:
      return
    papers = results.find_all("li", class_="list-result-item")

    for paper in papers:
        title = paper.find('h3', class_='title').find('span')
        author = paper.find('a', class_='link person')
        if author is None:
          author = ''
        else:
          author = author.find('span').text
        date = paper.find('span', class_="date")
        link = paper.find('h3', class_='title').find('a', href=True)['href']

        opening = pd.read_csv(CSV_NAME, index_col="Unnamed: 0")
        data = [title.text, author, date.text, link]
        df = pd.DataFrame([data], columns=['Title', 'Author', 'Published', 'Link'])
        df2 = pd.concat([df, opening], ignore_index=True)
        df2.to_csv(CSV_NAME)

def crawl(pages):
    i=0
    while True:
        if i > pages:
            break
        if i>0:
            url = URL + '?page=' + str(i)
        else:
            url = URL
        i = i+1
        # scraping starts here
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="main-content")
        researchers = results.find_all("li", class_="grid-result-item")

        for researcher in researchers:
            # Check if researcher has any papers
            check = researcher.find('div', class_='stacked-trend-widget')
            if check:
                name = check_department(researcher)
                if name is None:
                    pass
                else:
                  add_each_researchers_publication(name, PROFILE_URL)

create_csv()
pages = get_last_page()
crawl(pages)