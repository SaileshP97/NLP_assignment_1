import requests as re
from bs4 import BeautifulSoup
import pandas as pd

import json
import logging

import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.FileHandler("scraping_logs.log"),  # Logs saved to file
        logging.StreamHandler()  # Logs also displayed on the console
    ]
)

def get_base_url():

    base_url = {}
    with open('./base_url.json', 'rb') as f:

        base_url = json.load(f)
    return base_url

def update_base_url(base_url):

    with open('./base_url.json', 'w') as f:

        json.dump(base_url, f, indent=4)

def save_csv(dataframe, file):

    dataframe = dataframe.drop_duplicates().reset_index(drop=True)
    dataframe.to_csv(file, index=False)
    #dataframe.to_csv("./gujaratsamachar_text.csv", index=False)

def open_csv(file):

    return pd.read_csv(file)

def get_Links(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = re.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_boxes = soup.find_all('div', class_='news-box')

    links = []
    for box in news_boxes:
        a_tag = box.find('a')
        if a_tag and 'href' in a_tag.attrs:
            links.append(a_tag['href'])

    return links
    
def get_text(url):

    text = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = re.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    x = soup.find_all('p')
    for p in x:
        text.append(p.get_text())
    
    return text

def save_url_json(url_dict):

    with open("./gujaratsamachar_url.json", 'w') as f:
        json.dump(url_dict, f, indent=4)

def create_url_json(df):

    url_dict = {}

    for url in df['Links'].unique():
        url_dict[url] = 0

    with open("./gujaratsamachar_url.json", 'w') as f:
        json.dump(url_dict, f, indent=4)

def get_url_json(file):

    with open(file, 'r') as f:

        url_dict = json.load(f)
    return url_dict

def curate_url():

    try:
        df = open_csv('./gujaratsamachar_url.csv')
        links_list = list(df.loc[:,'Links'].unique())
    except FileNotFoundError:
        links_list = []

    base_urls = get_base_url()

    n_urls = 0

    for base_url in base_urls:

        if base_urls[base_url] == 1:
            continue

        i=1
        count = 0
        while(True):
            url = base_url + str(i)
            link = get_Links(url)
            if len(link)==0:
                if count>2:
                    break
                count+=1
                i+=1
                continue

            links_list = links_list + link
            i+=1

            n_urls+=1
            if n_urls%100==0:
                logging.info(f'Completed URL curation for {n_urls} Links')

        df = pd.DataFrame(links_list, columns=['Links'])

        create_url_json(df)
        save_csv(df, "./gujaratsamachar_url.csv")
        logging.info(f'Completed URL curation for {base_url}')

        base_urls[base_url] += 1
        update_base_url(base_urls)

def curate_text():

    url_dict = get_url_json("./gujaratsamachar_url.json")
    text_data = []
    count=1
    for url in url_dict.keys():
        if url_dict[url] == 1:
            continue
        base_url = "https://www.gujaratsamachar.com" + url
        text_data = text_data + get_text(base_url)
        if count%100 == 0:
            save_url_json(url_dict)
            logging.info(f'Processed {count} articles.')
            text_df = pd.DataFrame(text_data, columns=['text'])
            save_csv(text_df, "./gujaratsamachar_text.csv")
        count+=1
        url_dict[url] = 1

    text_df = pd.DataFrame(text_data, columns='text')
    save_csv(text_df, "./gujaratsamachar_text.csv")
    logging.info(f'Completed text curation.')

if __name__ == "__main__":

    logging.info('Starting URL curation...')
    curate_url()
    logging.info('Starting text curation...')
    curate_text()
    logging.info('Scraping completed.')




    