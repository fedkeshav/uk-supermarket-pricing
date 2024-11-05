import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import d_utils

class DataExtractor():
    '''
    ''' 
    def __init__(self):
        pass
        
    def extract_single_product_ocado_info(self, url):
        '''
        Returns all relevant info for a single product
        '''
        page = requests.get(url)
        html = page.text
        soup = BeautifulSoup(html, 'html.parser')
        # Finding product names
        headings = soup.find_all('div', {'class': 'fop-description'})
        product_names = []
        weights = []
        for x in range(len(headings)):
            details = headings[x].find_all('span')
            product_name = details[0].text
            weight = details[1].text
            product_names.append(product_name)
            weights.append(weight)

        # Finding the product prices
        price_headings = soup.find_all('div', class_= ['price-group-wrapper price-group-wrapper__value-delivered','price-group-wrapper'])
        delivered_prices = []
        for x in range(len(price_headings)):
            delivered_price = price_headings[x].find_all('span', class_=['fop-price fop-value-delivered','fop-price'])[0].text
            delivered_prices.append(delivered_price)
        
        df = pd.DataFrame({
            'product_names': product_names,
            'weights': weights,
            'delivered_prices': delivered_prices
        })
        return df

    def extract_all_ocado_info(self, common_url, df):
        '''
        Returns all relevant info for all products in question
        '''
        
        data = []
        for value in df['generic_product']:
            url = common_url + value
            new_df = self.extract_single_product_ocado_info(url)
            new_df['generic_product'] = value
            data.append(new_df)
            ocado_df = pd.concat(data, ignore_index=True)
        return ocado_df

    
    def extract_single_product_sainsbury_info(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        cookie_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All Cookies")]')))
        cookie_button.click()
        time.sleep(8)
        main_grid = driver.find_element(By.XPATH, value = '//ul[@class="ln-o-grid ln-o-grid--matrix ln-o-grid--equal-height"]')
        main_price = main_grid.find_elements(By.XPATH, value = '//div[@class="pt__cost"]')
        prices = []
        for x in range(len(main_price)):
            price = main_price[x].text
            prices.append(price)

        product_details = main_grid.find_elements(By.XPATH, '//h2[@class="pt__info__description"]')
        product_info = []
        for x in range(len(product_details)):
            info = product_details[x].text
            product_info.append(info)

        driver.quit()
        new_df = pd.DataFrame({
            'product_names': product_info,
            'prices': prices
            })
        return new_df
    
    def extract_all_sainsbury_info(self, common_url, df):
        sainsbury_data = []
        for value in df['generic_product']:
            url = common_url + value
            new_df = self.extract_single_product_sainsbury_info(url)
            new_df['generic_product'] = value
            sainsbury_data.append(new_df)
            sainsbury_df = pd.concat(sainsbury_data, ignore_index=True)
        return sainsbury_df

        