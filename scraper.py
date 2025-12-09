#https://sn.coinafrique.com/categorie/chiens

# import packages
from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_html(link):

  res = get(link)

  return bs(res.content)


def extract_containers(soup):

  containers = soup.find_all('div','col s6 m4 l3')

  return containers

def extract_item(container):

  name = container.find('p','ad__card-description').a.text

  #ad__card-price

  price = container.find('p','ad__card-price').text.replace('CFA','')


 # location
  location = container.find('p','ad__card-location').span.text

# URL ad__card-img
  url_image = container.find('img','ad__card-img').get('src')

  return {
      'name': name,
      'price': price,
      'location': location,
      'url_image': url_image
  }


def extract_page_items(containers):

  data = []
  for container in containers:
    data.append(extract_item(container))

  return data



#https://sn.coinafrique.com/categorie/chiens?page=2
def extract_website_items(base_url, page_start, page_end):

  data = []

  for page in range(page_start, page_end + 1):
    url = f"{base_url}?page={page}"
    soup = get_html(url)

    containers = extract_containers(soup)

    data.extend(extract_page_items(containers))

  return data   
