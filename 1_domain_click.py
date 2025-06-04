import pandas as pd
import gdown
import re
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gc
import time
import pytz
import datetime
import logging
from tqdm import tqdm
import traceback

df = pd.read_csv('suburbs.csv')

df.shape

def driver_setup():
  options = webdriver.FirefoxOptions()
  options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe' 
  options.add_argument('E:/Programs/geckodriver.exe')
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Firefox(options=options)
  return driver

def save_data_to_disk(data, filename):
    if os.path.isfile(filename):
        existing_df = pd.read_csv(filename)
        data = pd.concat([existing_df, data], ignore_index=True)
        os.remove(filename)
        data.to_csv(filename,index=False)
    else:
        data.to_csv(filename, mode='w', header=True, index=False)

log_filename = 'exemption_logs.txt'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

df['0'].to_list().index('west-mooreville-tas-7321')

fileind = 1

with open('dom_comp_'+str(fileind)+'.txt', 'r') as file:
    st_rng = int(file.read())

totlis = [0, 5293]
# st_rng = totlis[0]#---------------------
end_rng = totlis[1]
total_rng = abs(end_rng - st_rng)

pbar = tqdm(total=total_rng, desc='Searching', unit= f'query{fileind}')

for sub in range(st_rng, end_rng):
  pbar.update(1)

  url = 'https://www.domain.com.au/suburb-profile/'+df['0'][sub]
  driver = driver_setup()
  try:
    driver.get(url)
  except:
    driver = driver_setup()
    driver.get(url)
  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')
  table = soup.find("table")

  try:
    rows = table.find_all("tr")[1:]

    for row in range(len(rows)): 
        cells = rows[row].find_all("td")
        try:
          bedrooms = cells[0].text.strip()
        except:
          bedrooms = None
        try:
          prop_type = cells[1].text.strip()
        except:
          prop_type = None
        try:
          median_price = cells[2].text.strip()
        except:
          median_price = None
        try:
          days_on_market = cells[3].text.strip()
        except:
          days_on_market = None
        try:
          clearance_rate = cells[4].text.strip()
        except:
          clearance_rate = None
        try:
          sold_this_year = cells[5].text.strip()
        except:
          sold_this_year = None
        try:
          population = soup.find('div', {'class': 'css-48zwbo'}).find('div', {'class': 'css-54bw0x'}).text
        except:
          population = None
        try:
          average_age = soup.find_all('div', {'class': 'css-48zwbo'})[1].find('div', {'class': 'css-54bw0x'}).text
        except:
          average_age = None
        try:
          owner_percent = soup.find('span', {'data-testid': 'left-value'}).text.strip()
        except:
          owner_percent = None
        try:
          renter_percent = soup.find('span', {'data-testid': 'right-value'}).text.strip()
        except:
          renter_percent = None
        try:
          family_percent = soup.find_all('span', {'data-testid': 'left-value'})[1].text.strip()
        except:
          family_percent = None
        try:
          single_percent = soup.find_all('span', {'data-testid': 'right-value'})[1].text.strip()
        except:
          single_percent = None

        
        australia_timezone = pytz.timezone('Australia/Sydney')
        current_time = datetime.datetime.now(australia_timezone)

        

        row_data = { 
            "Bedrooms": bedrooms,
            "Type": prop_type,
            "Median Price": median_price,
            "Avg Days on Market": days_on_market,
            "Clearance Rate": clearance_rate,
            "Sold This Year": sold_this_year,
            'POPULATION': population,
            'AVERAGE AGE': average_age,
            'OWNER': owner_percent,
            'RENTER': renter_percent,
            'FAMILY': family_percent,
            'SINGLE': single_percent,
            'SUBURB': df['0'][sub],
            'Time_stamp': current_time
        }

        one_row_data = pd.DataFrame(row_data,index=[0])

        try:

          
          buttons = driver.find_elements(By.XPATH, "//button[@title='Open' or @title='Close']")
          WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Open' or @title='Close']")))
          buttons[row].click()


          button_html = buttons[row].get_attribute('outerHTML')
          soup = BeautifulSoup(button_html, 'html.parser')
          title_element = soup.find('div').find('title')
          title = title_element.get_text()
          print(title)
          html = driver.page_source
          soup = BeautifulSoup(html, 'html.parser')

          tr_element = soup.find('tr', class_='css-1wpy7ho')
          div_elements = tr_element.find_all('div', class_='css-15ydh5a')
          datad = {}

          
          for div in div_elements:
              h4_element = div.find('h4', class_='css-srsjf4')
              data_point = div.find('div', class_='css-1s6j0do')
              label = h4_element.text.strip(':')
              value = data_point.text.strip()
              datad[label] = value

          tdf = pd.DataFrame(datad, index=[0]) 

          table_rows = soup.find_all('tr')  
          data = {
              'Year': [],
              'Median Price': [],
              'Growth': [],
              'Number of Sales': []
          }
          for row in table_rows[1:]:
              columns = row.find_all('td')
              if len(columns) == 4:
                  year = columns[0].text.strip()
                  median_price = columns[1].text.strip()
                  growth = columns[2].text.strip()
                  num_sales = columns[3].text.strip()

                  data['Year'].append(year)
                  data['Median Price'].append(median_price)
                  data['Growth'].append(growth)
                  data['Number of Sales'].append(num_sales)

          yearly_df = pd.DataFrame(data)

          years = yearly_df['Year'].tolist()
          for year in years:
              tdf.loc[0, f'median_price_{year}'] = yearly_df.loc[yearly_df['Year'] == year, 'Median Price'].item()
              tdf.loc[0, f'growth_rate_{year}'] = yearly_df.loc[yearly_df['Year'] == year, 'Growth'].item()
              tdf.loc[0, f'no_of_sales_{year}'] = yearly_df.loc[yearly_df['Year'] == year, 'Number of Sales'].item()

          with open('dom_comp_'+str(fileind)+'.txt', 'w') as file:
            file.write(str(sub))
            
          tempdf = pd.concat([one_row_data, tdf], ignore_index=True)
          tempfilename = 'Domain_click_'+str(fileind)+'.csv'

          save_data_to_disk(tempdf, tempfilename)
          tempdf = pd.DataFrame()
          one_row_data = pd.DataFrame()
          
        except:
          None
  except:
    None

  try:
    driver.quit() 
  except:
    None