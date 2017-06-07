from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
import re
import pandas as pd
import traceback
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get('https://findapartner.hpe.com/')
sleep(3)
#To select type of partner
sel = Select(driver.find_element_by_css_selector('select#select-partner-type.partner_select'))
sel.select_by_visible_text('Find a Reseller Partner')
sleep(3)

#To get all the options for country names
cntrylst2 = []
optns = driver.find_element_by_xpath('//*[@id="search_country"]').text
cntrylst = "".join(list(optns)).split('\n')
for item in cntrylst:
    cntrylst2.append(item.strip())
cntrylst2 = list(filter(None,cntrylst2))
for idx,val in enumerate(cntrylst2):
    print(idx,val)
print('Enter the index number of the country you want to search for: ')
cntrynum = input()
title_ls = []
typprt_ls = []
prtsp_ls = []
address_ls = []
phnum_ls = []
email_ls = []
distnct_spec = []
cntry = []
head = 0
   
selcntry = Select(driver.find_element_by_xpath('//*[@id="search_country"]'))
selcntry.select_by_visible_text(str(cntrylst2[int(cntrynum)]))
sleep(3)
print('Enter name of city: ')
city = input()
elem = driver.find_element_by_css_selector('input#input-location.form-control.input.search-box')
elem.clear()
elem.send_keys(str(city))
elem.send_keys(Keys.ARROW_DOWN)
elem.send_keys(Keys.RETURN)
sleep(3)
try:
    driver.find_element_by_xpath('//*[@id="filter-partner-results"]').click()
    sleep(3)
    driver.find_element_by_xpath('//*[@id="locatorFilterCollapse"]/div/div/section/header/section/div/div/div[3]/label[1]').click()
    driver.find_element_by_xpath('//*[@id="Products-tab-toggle"]').click()
    driver.find_element_by_xpath('//*[@id="Storage-tab-toggle"]').click()
    sleep(3)
    driver.find_element_by_xpath('//*[@id="hpe-partner-subcategory-Storage"]/section/section/div[1]').click()
    driver.find_element_by_xpath('//*[@id="hpe-apply-selected-filters"]').click()
    sleep(3)
except Exception:
    traceback.print_exc()
try:
    pages = driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[4]/ul/li[2]')
    pages2 = re.search('of (\d+)',str(pages.text)).group(0)
    pg2 = pages2.split()[1]
except Exception:
    pg2 = 1
    traceback.print_exc()
head = 0
for j in list(range(int(pg2))):   
    for i in list(range(1,40)):
        dftitle = pd.DataFrame()
        dftypprt = pd.DataFrame()
        dfprtsp = pd.DataFrame()
        dfaddr = pd.DataFrame()
        dffinal = pd.DataFrame()
        dfph = pd.DataFrame()
        dfem = pd.DataFrame()
        try:
            driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[2]/ul/li['+str(i)+']').click()
            sleep(3)
            for it in list(range(1,3)):
                try:
                    title = driver.find_element_by_xpath('//*[@id="more-info-panel"]/article/header/h2['+str(it)+']')
                    title_ls.append(str(title.text))
                    print(title.text)
                except Exception:
                    traceback.print_exc()
            typprt = driver.find_element_by_css_selector('h6.text-muted')
            typprt_ls.append(str(typprt.text))
            addr = driver.find_element_by_xpath('//*[@id="more-info-panel"]/article/main/address/div[1]').text
            address_ls = "".join(list(addr)).split('\n')
            prtspec = driver.find_element_by_xpath('//*[@id="more-info-panel"]/article/main/aside/div[2]/ul').text
            prtsp_ls = "".join(list(prtspec)).split('\n')
            for item in prtsp_ls:
                distnct_spec.append(item)
            phnum = driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[2]/ul/li[1]/div[1]/div[2]/h4')
            phnum_ls.append(phnum.text)
            email = driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[2]/ul/li[1]/div[1]/div[2]/h5/a')
            email_ls.append(email.text)
            dftitle['title'] = title_ls
            dftypprt['type of prt'] = typprt_ls
            dfprtsp['specialization'] = prtsp_ls
            dfaddr['addrs'] = address_ls
            dfph['Number'] = phnum_ls
            dfem['Email'] = email_ls
            dffinal = pd.concat([dftitle,dftypprt,dfprtsp,dfaddr,dfph,dfem],ignore_index = True, axis = 1)
            dffinal.columns = ['Company Name','Type of Partner','Partner Specs','Address','Contact Number','Email']
        except Exception:
            traceback.print_exc()
        csvfl = open('PrtnrLst.csv','a',encoding='utf-8')
        if head == 0:
            dffinal.to_csv(csvfl,index = None)
        else:
            dffinal.to_csv(csvfl,header = False,index = None)
        csvfl.close()
        head = head + 1
        del title_ls[:]
        del typprt_ls[:]
        del prtsp_ls[:]
        del address_ls[:]
        del cntry[:]
        del dftitle 
        del dftypprt
        del dfprtsp
        del dfaddr
        del dffinal
        del dfph
        del dfem
        del phnum_ls[:]
        del email_ls[:]
            
    try:                
        driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[4]/ul/li[3]/a').click()
    except Exception:
        print('No Next Page')
        traceback.print_exc()
driver.quit()
