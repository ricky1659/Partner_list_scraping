from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
import re
import pandas as pd
import traceback
from selenium.webdriver.common.keys import Keys
from tkinter import Tk
from tkinter import filedialog


root = Tk()
root.filename = filedialog.askopenfilename(filetype = (('Comma Separated Values','*.csv'),('All File','*.*')),title = 'Select Imput File')
ipfile = open(str(root.filename),'r')
root.destroy()
ipdf = pd.read_csv(ipfile,encoding = 'utf-8')

cntry_names = list(ipdf.columns.values)
path = r"C:\Python35-32\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get('https://findapartner.hpe.com/')
sleep(3)
#To select type of partner
sel = Select(driver.find_element_by_css_selector('select#select-partner-type.partner_select'))
sel.select_by_visible_text('Find a Reseller Partner')
sleep(3)


title_ls = []
typprt_ls = []
prtsp_ls = []
address_ls = []
phnum_ls = []
email_ls = []
distnct_spec = []
cntry = []
pncd = []
head = 0
   
for country in cntry_names:
    for pincodes in list(ipdf[country]):
        #country name matching
        sel2 = Select(driver.find_element_by_css_selector('select#search_country'))
        sel2.select_by_visible_text(str(country.strip()))

        #sending inputs for pincodes                             
        elem = driver.find_element_by_css_selector('input#input-location.form-control.input.search-box')
        elem.clear()
        elem.send_keys(str(pincodes))
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
                                           
        for j in list(range(int(pg2))):   
            for i in list(range(1,40)):#seq from 1 to 40 because xpath takes random number between them
                dftitle = pd.DataFrame()
                dftypprt = pd.DataFrame()
                dfprtsp = pd.DataFrame()
                dfaddr = pd.DataFrame()
                dffinal = pd.DataFrame()
                dfph = pd.DataFrame()
                dfem = pd.DataFrame()
                dfcntry = pd.DataFrame()
                dfpncd = pd.DataFrame()
                #clicking on results
                try:
                    driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[2]/ul/li['+str(i)+']').click()
                    sleep(3)
                    for it in list(range(1,3)):#get title names, 1 to 3 because xpath takes random 
                        try:
                            title = driver.find_element_by_xpath('//*[@id="more-info-panel"]/article/header/h2['+str(it)+']')
                            title_ls.append(str(title.text))
                            print(title.text)
                        except Exception:
                            traceback.print_exc()
                    #to get the partner type
                    typprt = driver.find_element_by_css_selector('h6.text-muted')
                    typprt_ls.append(str(typprt.text))
                    cntry.append(str(country))#country names
                    pncd.append(str(pincodes))
                    #to get the address
                    addr = driver.find_element_by_xpath('//*[@id="more-info-panel"]/article/main/address/div[1]').text
                    address_ls = "".join(list(addr)).split('\n')
                    #to get partner specialization
                    prtspec = driver.find_element_by_xpath('//*[@id="more-info-panel"]/article/main/aside/div[2]/ul').text
                    prtsp_ls = "".join(list(prtspec)).split('\n')
                    for item in prtsp_ls:
                        distnct_spec.append(item)
                    #to get phone numbers 
                    phnum = driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[2]/ul/li[1]/div[1]/div[2]/h4')
                    phnum_ls.append(phnum.text)
                    #to get emails
                    email = driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[2]/ul/li[1]/div[1]/div[2]/h5/a')
                    email_ls.append(email.text)
                                           
                    dftitle['title'] = title_ls
                    dftypprt['type of prt'] = typprt_ls
                    dfprtsp['specialization'] = prtsp_ls
                    dfaddr['addrs'] = address_ls
                    dfph['Number'] = phnum_ls
                    dfem['Email'] = email_ls
                    dfcntry['country'] = cntry
                    dfpncd['pincode'] = pncd                       
                    dffinal = pd.concat([dftitle,dftypprt,dfprtsp,dfaddr,dfph,dfem,dfcntry,dfpncd],ignore_index = True, axis = 1)
                    dffinal.columns = ['Company Name','Type of Partner','Partner Specs','Address','Contact Number','Email','Country Name','Pincode']
                except Exception:
                    traceback.print_exc()
                csvfl = open('PrtnrLst_pincode.csv','a',encoding='utf-8')
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
                del pncd[:]                           
                del dftitle 
                del dftypprt
                del dfprtsp
                del dfaddr
                del dffinal
                del dfph
                del dfem
                del dfcntry
                del dfpncd                           
                del phnum_ls[:]
                del email_ls[:]
            
            try:                
                driver.find_element_by_xpath('//*[@id="results-overlay-list-accordion"]/div[4]/ul/li[3]/a').click()
            except Exception:
                print('No Next Page')
                traceback.print_exc()
driver.quit()
