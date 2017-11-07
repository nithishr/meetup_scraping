# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import logging


class TelefonbuchSpider(scrapy.Spider):
    name = 'telefonbuch'
    allowed_domains = ['bundes-telefonbuch.de']
    start_urls = ['http://bundes-telefonbuch.de/']

    # Handle the Command line arguments
    def __init__(self, sector=None, city=None, *args, **kwargs):
        super(TelefonbuchSpider, self).__init__(*args, **kwargs)
        self.sector = sector
        self.city = city
        self.page_count = 2
        self.pages = 0


    # Handle the homepage
    def parse(self, response):
        logging.info('Scraping {0} in {1}'.format(self.sector,self.city))
        request = scrapy.FormRequest.from_response(response, formid = 'searchForm', formdata = {'what':self.sector, 'where':self.city}, callback = self.parse_results)
        yield request


    # Handle the results from the form submission
    def parse_results(self, response):
        results_soup = BeautifulSoup(response.text,'html.parser')
        entries = results_soup.find_all('div', {'class':'companyBox'})
        self.pages += 1
        if self.pages > self.page_count:
            return
        for entry in entries:
            entry_url = entry.a.get('href')
            contact_info  = scrapy.http.Request(url = self.start_urls[0] + entry_url, callback = self.parse_contact)
            yield contact_info

        # Obtain the next page to scrape if it exists
        paging = results_soup.find('div',{'id':'pagination'})
        pages = paging.find_all('a')
        next_page = None
        for page in pages:
            if page.text.strip()=='∨':
                next_page = page.get('href')
                break

        if next_page is not None :
            yield scrapy.http.Request(url = self.start_urls[0] + next_page, callback = self.parse_results)


    # Handle the individual result
    def parse_contact(self, response):
        entry_soup = BeautifulSoup(response.text,'html.parser')

        try:
            name = entry_soup.h1.text.strip()
        except:
            name = ''

        try:
            address_div = entry_soup.find('div',{'class':'detail-address'})
            address_parts = list(address_div.stripped_strings)
            address = ' '.join(address_parts)
        except:
            address = ''

        try:
            email_link = entry_soup.find('a',{'class':'detail-email'}).get('href')
            email = email_link.split(':')[-1]
        except:
            email = ''

        try:
            website = entry_soup.find('a',{'class':'detail-homepage'}).get('href')
        except:
            website = ''

        try:
            telephone = entry_soup.find('span', {'class':'detail-phone'}).text.strip()
        except:
            telephone = ''

        try:
            fax = entry_soup.find('span', {'class':'detail-fax'}).text.strip()
        except:
            fax = ''

        yield {'Name':name, 'Address':address, 'Website':website, 'Email':email, 'Phone No':telephone, 'Fax': fax}