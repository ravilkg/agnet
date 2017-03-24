import unittest
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from bs4 import BeautifulSoup
import requests
import csv
from random import choice
from random import uniform
from multiprocessing import Pool

dcap = dict(DesiredCapabilities.PHANTOMJS)
# url = 'https://www.avtogid.kg/browse/Auto/?sorting_fields[activation_date]=DESC'
url_ag = 'https://www.avtogid.kg/'
# make = 'Mercedes-Benz'
# dcap["proxy.httpProxy"] = ("119.163.121.122:8080")
# dcap["proxy.proxyType"] = ("http")
# dcap["phantomjs.page.settings.userAgent"] = (
#      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)")


class TestUbuntuHomepage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.set_window_size(1024, 768)
        print(dcap)


    def testTitle(self):
        self.driver.get('http://sitespy.ru/my-ip')
        self.assertIn('Узнать мой ip адрес', self.driver.title)
        self.driver.get_screenshot_as_file('test.png')


    def tearDown(self):
        self.driver.quit()


class Bot:
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        # self.driver.set_window_size(360, 640)
        self.driver.set_window_size(1024, 768)
        # self.navigate()

    def take_screenshot(self):
        self.driver.save_screenshot('ag_screenshot.png')

    def search_main(self, url, query):
        self.driver.get(url)
        self.driver.find_element_by_xpath(
            '//input[@class="form-control stringWithAutocomplete keywords ui-autocomplete-input"]').send_keys(query)
        search = self.driver.find_element_by_xpath('//input[@class="btn btn-primary"]')
        search.click()
        sleep(uniform(5,15))
        return self.driver.current_url

    def next_page(self, url):
        self.driver.get(url)
        self.driver.find_element_by_xpath('//a[@class="nextPageSelector"]').click()
        sleep(uniform(5,10))
        print(self.driver.current_url)
        return self.driver.current_url

    def find_all_items(self, url):
        self.driver.get(url)
        collect = self.driver.find_element_by_xpath('//div[@class="searchResults"]')
        allItems = collect.find_elements_by_xpath('//a[@class="listingimgurl"]')
        for item in allItems:
            link = item.get_attribute("href")
            print(link)

    def navigate(self, url):
        print('open page: ')
        self.driver.get(url)
        print(self.driver.current_url)
        sleep(uniform(120, 240))
        print('press phone #: ')
        self.driver.find_element_by_xpath('//span[@class="btn btn-primary"]').click()
        sleep(uniform(30, 120))
        # self.driver.back()

    def get_netkg_id(self, url):
        self.driver.get(url)
        netkg = self.driver.find_element_by_xpath('//img[@class="netkgimg"]').get_attribute("src")
        print(netkg)

def get_html(url):
    r = requests.get(url)
    print('get HTML from search page:')
    return r.text

def random_queries():
    queries = open('queries.txt').read().split('\n')
    query = choice(queries)
    print('send query:' + query)
    return query

#записать в файл CSV
def write_csv(data):
    with open('search_page_links.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data,))

#получить все ссылки со страницы
def get_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_= 'searchResults').find_all('div', class_='caption')
    links = []
    for ad in ads:
        link = 'https://www.avtogid.kg' + ad.find('a').get('href')
        print(link)
        links.append(link)
        write_csv(link)

    return links

#получить ID поискового запроса, параметр HTML страницы
def get_search_id(html):
    soup = BeautifulSoup(html, 'lxml')
    base = soup.find('ul', class_='pagination').find_all('li')[-1].find_previous_sibling('li')
    searchid = base.find('a').get('href').split('&')[1].strip()

    return searchid

def get_last_page(html):
    soup = BeautifulSoup(html, 'lxml')
    base = soup.find('ul', class_='pagination').find_all('li')[-1].find_previous_sibling('li')
    pages = base.text.strip()

    return int(pages)

def surfing(url):
    b = Bot()
    b.navigate(url)

def main():
    b = Bot()
    for i in range(1000):
        url = b.search_main(url_ag, random_queries())
        try:
            html = get_html(url)
            all_links = get_urls(html)

            with Pool(10) as p:
                p.map(surfing, all_links)

        except:
            continue

    # csv_links = []
    # with open('search_page_links.csv') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         csv_links.append(' '.join(row))
    #
    #     print(csv_links)
    #
    # with Pool as p:
    #     p.map(b.navigate, csv_links)





if __name__ == '__main__':
    # unittest.main(verbosity=2)
    main()