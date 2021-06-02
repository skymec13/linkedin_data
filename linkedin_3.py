from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common import action_chains, keys
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import unicodedata
import csv
from selenium.webdriver.support.ui import Select
import parameters
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

options = Options()
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

user_agent = random.choice(user_agent_list)
user_agent
options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(ChromeDriverManager().install(), options = options)
browser.delete_all_cookies()


browser.get('https://www.linkedin.com')
try:
    loginPageBTN = browser.find_element_by_xpath('/html/body/nav/div/a[2]')
except:
    loginPageBTN = browser.find_element_by_xpath('/html/body/nav/div/a')


print("login page will load shortly")
loginPageBTN.click()
sleep(1)
username = browser.find_element_by_id('username')
print("username input located")
username.send_keys(parameters.linkedin_username)
sleep(0.5)
password = browser.find_element_by_id('password')
print("password input located")
password.send_keys(parameters.linkedin_password)
sleep(0.5)
password.submit()
print("logged in successfully")
sleep(0.5)

while(1):
    try:
        print ('Enter links file name')
        fName= input()
        file=open(str(fName)+'.csv', "r")
        print ('File read successfully.')
        break
    except:
        print ('Error reading file.')

reader = csv.reader(file)
links=list()

for line in reader:
    for col in line:
        links.append(col)
del links[0]
#print(links)
print (str(len(links))+' links found in file.')

print ('Enter output file name:')
oName= input()
open(str(oName)+'.csv',"w")
print(str(oName)+'.csv file created successfully')
print ('Starting scrape now.')


data=list()
count=0
check = 0
count1 = 0
for link in links:
    count+=1
    if count > 11 and count < 16:
        print ('Record count: '+str(count))
        try:
            browser.get(link)
            check = 1
            
            SCROLL_PAUSE_TIME = 0.5
            last_height = browser.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            soup = BeautifulSoup(browser.page_source,'lxml')
            
            try:
                browser.find_element_by_class_name("pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle artdeco-button artdeco-button--tertiary artdeco-button--muted").click()
                time.sleep(4)
            except:
                print('Error expanding more see more experience using 1')
            
            
            
            d = list()
            d.append(link)
            d.append('0')
            d.append(soup.find('div',{'class':'pv-text-details__left-panel mr5'}).find('h1').get_text().strip())
            try:
                d.append(soup.find('div',{'class':'pv-text-details__left-panel mr5'}).find('span',{'class':'dist-value'}).get_text().strip())
            except:
                d.append(' ')
            print(d)


            ########### Experience
            experiences=list()
            exp=soup.find('section',{'id':'experience-section'}).find_all('section',{'class':'pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view'})
            for ex in exp:
                if 'Company Name' in ex.find('h3',{'class':'t-16 t-black t-bold'}).get_text().strip():
                    name=ex.find('h3',{'class':'t-16 t-black t-bold'}).find_all('span')[-1].get_text().strip()
                    for li in ex.find_all('li'):
                        try:
                            experiences.append(li.find('h3',{'class':'t-14 t-black t-bold'}).find_all('span')[-1].get_text().strip())
                        except:
                            experiences.append(' ')
                        try:
                            experiences.append(name)
                        except:
                            expreriences.append(' ')
                        try:
                            experiences.append(li.find('h4',{'class':'pv-entity__date-range t-14 t-black--light t-normal'}).find_all('span')[1].get_text().strip().split('–')[0].strip())
                        except:
                            experiences.append(' ')
                        try:
                            experiences.append(li.find('h4',{'class':'pv-entity__date-range t-14 t-black--light t-normal'}).find_all('span')[1].get_text().strip().split('–')[1].strip())
                        except:
                            experiences.append(' ')
                        try:
                            experiences.append(li.find('h4',{'class':'t-14 t-black--light t-normal'}).find_all('span')[-1].get_text().strip())
                        except:
                            experiences.append(' ')
                        try:
                            experiences.append(li.find('h4',{'class':'pv-entity__location t-14 t-black--light t-normal block'}).find_all('span')[-1].get_text().strip())
                        except:
                            experiences.append(' ')
                        try:

                            experiences.append(li.find('p',{'class':'pv-entity__description t-14 t-black t-normal inline-show-more-text inline-show-more-text--is-collapsed ember-view'}).get_text(separator = " ").strip())
                        except:
                            experiences.append(' ')
                        #print (' ')

                else:  
                    try:
                        experiences.append(ex.find('h3',{'class':'t-16 t-black t-bold'}).get_text().strip())
                    except:
                        experiences.append(' ')
                    try:
                        experiences.append(ex.find('p',{'class':'pv-entity__secondary-title t-14 t-black t-normal'}).get_text().strip())
                    except:
                        experiences.append(' ')
                    try:
                        experiences.append(ex.find('h4',{'class':'pv-entity__date-range t-14 t-black--light t-normal'}).find_all('span')[1].get_text().strip().split('–')[0].strip())
                    except:
                        experiences.append(' ')
                    try:
                        experiences.append(ex.find('h4',{'class':'pv-entity__date-range t-14 t-black--light t-normal'}).find_all('span')[1].get_text().strip().split('–')[1].strip())
                    except:
                        experiences.append(' ')
                    try:
                        experiences.append(ex.find('h4',{'class':'t-14 t-black--light t-normal'}).find_all('span')[-1].get_text().strip())
                    except:
                        experiences.append(' ')
                    try:
                        experiences.append(ex.find('h4',{'class':'pv-entity__location t-14 t-black--light t-normal block'}).find_all('span')[-1].get_text().strip())
                    except:
                        experiences.append(' ')
                    try:
                        experiences.append(ex.find('p',{'class':'pv-entity__description t-14 t-black t-normal inline-show-more-text inline-show-more-text--is-collapsed ember-view'}).get_text(separator = " ").strip())
                    except:
                        experiences.append(' ')




            for temp in range(140-len(experiences)):
                experiences.append(' ')
            for e in range(140):
                d.append(experiences[e])

            sleep(0.5)
            ################## EDUCATION
            try:
                educations=list()
                edu=(soup.find('section',{'id':'education-section'}).find_all('a',{'data-control-name':'background_details_school'}))
                for ed in edu:
                    try:
                        educations.append(ed.find('h3',{'class':'pv-entity__school-name t-16 t-black t-bold'}).get_text().strip())
                    except:
                        educaations.append(' ')
                    try:
                        educations.append(ed.find('p',{'class':'pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal'}).find_all('span')[-1].get_text().strip())
                    except:
                        educations.append(' ')
                    try:
                        educations.append(ed.find('p',{'class':'pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal'}).find_all('span')[-1].get_text().strip())
                    except:
                        educations.append(' ')
                    try:
                        educations.append(ed.find('p',{'class':'pv-entity__dates t-14 t-black--light t-normal'}).find_all('span')[-1].get_text().strip().split('–')[0].strip())
                    except:
                        educations.append(' ')
                    try:
                        educations.append(ed.find('p',{'class':'pv-entity__dates t-14 t-black--light t-normal'}).find_all('span')[-1].get_text().strip().split('–')[1].strip())
                    except:
                        educations.append(' ')

                for temp in range(50-len(educations)):
                    educations.append(' ')
                for e in range(50):
                    d.append(educations[e])
                data.append(d)
                del d 
                sleep(0.5)
            except:
                continue
        except:
            d=list()
            d.append(link)
            d.append('1')
            if check == 2:
                count1 += 1
            check = 2 
            data.append(d)
            del d

        if count1 > 5:
            print("more than 5 profiles missing")
            break

        try:
            print ('Number of links scraped: '+str(len(data)))
            df = pd.DataFrame(data,columns=['Link','Missing','Title','Distance','Position_1','Company_1','StartDate_1','EndDate_1','Duration_1','Location_1','Description_1','Position_2','Company_2','StartDate_2','EndDate_2','Duration_2','Location_2','Description_2','Position_3','Company_3','StartDate_3','EndDate_3','Duration_3','Location_3','Description_3','Position_4','Company_4','StartDate_4','EndDate_4','Duration_4','Location_4','Description_4','Position_5','Company_5','StartDate_5','EndDate_5','Duration_5','Location_5','Description_5','Position_6','Company_6','StartDate_6','EndDate_6','Duration_6','Location_6','Description_6','Position_7','Company_7','StartDate_7','EndDate_7','Duration_7','Location_7','Description_7','Position_8','Company_8','StartDate_8','EndDate_8','Duration_8','Location_8','Description_8','Position_9','Company_9','StartDate_9','EndDate_9','Duration_9','Location_9','Description_9','Position_10','Company_10','StartDate_10','EndDate_10','Duration_10','Location_10','Description_10','Position_11','Company_11','StartDate_11','EndDate_11','Duration_11','Location_11','Description_11','Position_12','Company_12','StartDate_12','EndDate_12','Duration_12','Location_12','Description_12','Position_13','Company_13','StartDate_13','EndDate_13','Duration_13','Location_13','Description_13','Position_14','Company_14','StartDate_14','EndDate_14','Duration_14','Location_14','Description_14','Position_15','Company_15','StartDate_15','EndDate_15','Duration_15','Location_15','Description_15','Position_16','Company_16','StartDate_16','EndDate_16','Duration_16','Location_16','Description_16','Position_17','Company_17','StartDate_17','EndDate_17','Duration_17','Location_17','Description_17','Position_18','Company_18','StartDate_18','EndDate_18','Duration_18','Location_18','Description_18','Position_19','Company_19','StartDate_19','EndDate_19','Duration_19','Location_19','Description_19','Position_20','Company_20','StartDate_20','EndDate_20','Duration_20','Location_20','Description_20','InstitutionName_1','DegreeName_1','FieldOfStudy_1','StartDate_1','EndDate_1','InstitutionName_2','DegreeName_2','FieldOfStudy_2','StartDate_2','EndDate_2','InstitutionName_3','DegreeName_3','FieldOfStudy_3','StartDate_3','EndDate_3','InstitutionName_4','DegreeName_4','FieldOfStudy_4','StartDate_4','EndDate_4','InstitutionName_5','DegreeName_5','FieldOfStudy_5','StartDate_5','EndDate_5','InstitutionName_6','DegreeName_6','FieldOfStudy_6','StartDate_6','EndDate_6','InstitutionName_7','DegreeName_7','FieldOfStudy_7','StartDate_7','EndDate_7','InstitutionName_8','DegreeName_8','FieldOfStudy_8','StartDate_8','EndDate_8','InstitutionName_9','DegreeName_9','FieldOfStudy_9','StartDate_9','EndDate_9','InstitutionName_10','DegreeName_10','FieldOfStudy_10','StartDate_10','EndDate_10'])
            df.to_csv(str(oName)+'.csv')
            print ('File updated.')
        except:
            temp='none'
        
    
#css = "button[class = 'nav-item__link nav-item__dropdown-trigger t-14 t-black--light t-bold artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view']"
#drop = browser.find_element_by_css_selector(css)
#drop.click()


#css = "a[data-control-name = 'nav.settings_signout']"
#signout = browser.find_element_by_css_selector(css)
#signout.click()


#print("signed out")
##sleep(120)
print ('Closing browser now')
browser.quit()



