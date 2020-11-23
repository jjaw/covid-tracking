from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pprint
import csv
import gspread
import requests
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from socket import gaierror
import time
import os
import pytesseract #change text to image
from PIL import Image
from datetime import date

#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install())

#California data
url = "https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/SNFsCOVID_19.aspx"

driver.get(url)

#find the tableau table
element = driver.find_element_by_xpath("//iframe[@title='Data Visualization']")

#url of tableau table
new_url = element.get_attribute("src")

#HTMLSession token
sess = HTMLSession()

#dashboard URL 11/20
#test_url = "https://datavisualization.cdph.ca.gov/t/LNC/views/COVIDSNFDASHV3/COVIDSNFDASH?:isGuestRedirectFromVizportal=y&:embed=y"

r = sess.get(new_url)
r.html.render(timeout=16, sleep=8)
print("tableu_table_status:", r.status_code)

#find all the images
test = r.html.find("div img")

#base url to extract the image
base_url = "https://datavisualization.cdph.ca.gov"

src = "src"
image_urls = []

for x in test:
  #check to see if the element has src attribute 
  if src in x.attrs.keys(): 
    image_urls.append(x.attrs["src"])
    print(x.attrs["src"], "appended")
  else:
    print("nothing here")

#get the link for each of the images
for i, x in enumerate(image_urls):
  image_urls[i] = base_url + x

#changing image url to nested link for csv file rows
images = []
for x in image_urls:
  images.append([x]) 


#take out the blank images
search_image_urls = []
blank = "blank" #don't want blank, put it in search
for image in images:
  image = "".join(image)
  if blank in image:
    pass
  else:
    #search_image_urls has all the cleaned image url in str format
    search_image_urls.append(image)

#download the images



#recognize image then print get the test

pictures = []
for i, search_image_url in enumerate(search_image_urls):
  try:
    r = requests.get(search_image_url)
  #time.sleep(5)
    with open("ca/" + str(i)+".png", "wb") as f:
      f.write(r.content)
  except (gaierror, NewConnectionError, MaxRetryError, ConnectionError) as err:
    raise ValueError("Didn't load... " + "ca/" + str(i) + ".png")
  

#create a list to store all the texts recognized from the images
texts = []

#get the text from image through tesseract
for x in range(len(search_image_urls)):

  #making sure we don't get an extra file b/c of indexing
  if  x != range(len(search_image_urls)):
    
    output_file = "ca/" + str(x) + ".png"

    #this is the config setting that works with the number we need
    text = pytesseract.image_to_string(Image.open(output_file), config="-c -tessedit_char_whitelist=0123456789 --oem 0 --psm 8")
    texts.append(text.strip().replace(",", ""))
    #print(text)

#strip the blanks from the list of texts
while ("" in texts):
  texts.remove("")
pprint.pprint(texts)

#record of all the links to a csv file
with open("ca/ca.csv", "w", newline="") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(images)

#data we want, this part is hardcoded for now.. need to change later on

output = [
  ["NURSING HOME " + str(date.today())],
  ["Resident Positives", int(texts[3])],
  ["Resident Deaths Nursing Homes", int(texts[5])],
  ["Staff Positives Nursing Home", int(texts[11])],
  ["Staff Deaths Nursing Homes", int(texts[13])], 
  ["Skilled Nursing Facilities", int(texts[0])]
]
"""
#print it out horizontally
output = [
  ["NURSING HOME " + str(date.today()), "Resident Positives", "Resient Deaths Nursing Homes", "Staff Positives Nursing Home", "Staff Deaths Nursing Homes", "Skilled Nursing Facilities"],
  ["", int(texts[3]), int(texts[5]), int(texts[11]), int(texts[13]), int(texts[0])]
]
"""

print ("*************OUTPUT**************")
print(output)
#random table
#/vizql/v_201942006261424/javascripts/built-dojo/dojo/resources/blank.gif 


#writing img url to google sheet

gc = gspread.service_account()

#this is a pesonal sheet for testing
sh = gc.open("covid-test")

sh.sheet1.insert_rows(output)